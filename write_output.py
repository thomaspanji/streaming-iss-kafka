from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.functions import from_unixtime
from pyspark.sql.types import (
    StringType, 
    IntegerType,
    StructField,
    StructType,
)

spark = SparkSession \
    .builder \
    .appName("PySpark-Kafka ISS-location") \
    .getOrCreate()

spark.conf.set("spark.sql.streaming.checkpointLocation", '/home/thomas/checkpoint')

KAFKA_TOPIC = 'iss-location'
KAFKA_BOOTSTRAP_SERVER = 'localhost:9092'
DESTINATION_FOLDER = '/home/thomas/iss-output'


df = spark.readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers',KAFKA_BOOTSTRAP_SERVER) \
    .option('subscribe',KAFKA_TOPIC) \
    .load() 

# +----+--------------------+------------+---------+------+--------------------+-------------+
# | key|               value|       topic|partition|offset|           timestamp|timestampType|
# +----+--------------------+------------+---------+------+--------------------+-------------+
# |null|[7B 22 6D 65 73 7...|iss-location|        0|   214|2022-03-11 15:51:...|            0|
# +----+--------------------+------------+---------+------+--------------------+-------------+

schema2 = StructType([
    StructField('timestamp', IntegerType(), True),
    StructField('message', StringType(), True),
    StructField('iss_position', StructType([
                    StructField('longitude',StringType(),True),
                    StructField('latitude',StringType(), True)
                ])
    )
])

df_1 = df.withColumn('val',from_json(col('value').cast('string'), schema=schema2)) \
    .select('val.*')

# +----------+-------+-------------------+
# | timestamp|message|       iss_position|
# +----------+-------+-------------------+
# |1646998746|success|{88.2350, -30.9153}|
# +----------+-------+-------------------+

df_2 = df_1.select('timestamp','iss_position.*')

# +----------+---------+--------+
# | timestamp|longitude|latitude|
# +----------+---------+--------+
# |1647003363| -12.7691|-49.9196|
# +----------+---------+--------+

df_3 = df_2 \
    .withColumn('ISO_time', from_unixtime('timestamp')) \
    .select('ISO_time', 'longitude', 'latitude')


df_3.writeStream \
    .format("csv") \
    .option("path", DESTINATION_FOLDER) \
    .option("header", "true") \
    .trigger(processingTime="1 minute") \
    .start() \
    .awaitTermination()