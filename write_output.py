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
    .appName("PySpark-Kafka for streaming ISS location") \
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

# Default schema when reading data from Kafka source.
# Note that the actual data we need is store in `value` column,
# which is stored as a binary data.
# +----+--------------------+------------+---------+------+--------------------+-------------+
# | key|               value|       topic|partition|offset|           timestamp|timestampType|
# +----+--------------------+------------+---------+------+--------------------+-------------+
# |null|[7B 22 6D 65 73 7...|iss-location|        0|   214|2022-03-11 15:51:...|            0|
# +----+--------------------+------------+---------+------+--------------------+-------------+

# Define the schema of actual data refer to the JSON output from the API
schema = StructType([
    StructField('timestamp', IntegerType(), True),
    StructField('message', StringType(), True),
    StructField('iss_position', StructType([
                    StructField('longitude',StringType(),True),
                    StructField('latitude',StringType(), True)
                ])
    )
])

# Extract `value` column and cast as a string,
# so the content will be human-readable.
df_1 = df \
    .withColumn('val',from_json(col('value').cast('string'), schema=schema)) \
    .select('val.*')

# The dataframe will be looked like this 
# +----------+-------+-------------------+
# | timestamp|message|       iss_position|
# +----------+-------+-------------------+
# |1646998746|success|{88.2350, -30.9153}|
# +----------+-------+-------------------+

# Select the content of iss_position by using asterisk (*) symbol.
# This is how to "unpack" StructType column.
df_2 = df_1.select('timestamp','iss_position.*')

# The dataframe then will be looked like this.
# Note the column names.
# +----------+---------+--------+
# | timestamp|longitude|latitude|
# +----------+---------+--------+
# |1647003363| -12.7691|-49.9196|
# +----------+---------+--------+

# If unspecified in Spark configuration,
# the default time zone is our local time zone.
df_3 = df_2 \
    .withColumn('local_time', from_unixtime('timestamp')) \
    .select('local_time', 'longitude', 'latitude')

# Write data into CSV files every one minute to specified folder.
df_3.writeStream \
    .format("csv") \
    .option("path", DESTINATION_FOLDER) \
    .option("header", "true") \
    .trigger(processingTime="1 minute") \
    .start() \
    .awaitTermination()