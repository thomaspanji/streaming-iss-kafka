# Streaming ISS Position Data using Kafka

## Scope of work

This project aims to consume real-time International Space Station (ISS) position data from [Open Notify API Server](http://api.open-notify.org/iss-now.json) and save the data into CSV format files.

I use Apache Kafka to stream the data and leverage the Kafka Producer API for Python. The documentation and how to install this API is available [here](https://kafka-python.readthedocs.io/en/master/). The data received will be processed immediately using a Spark application and stored in a local computer.

This is a raw look when opening the link in the browser. The data is a nested JSON formatted.
![raw-look](/img/raw-json.png)


## Script

I created two main Python files: `simple_kafka_producer.py` and `write_output.py`. The first is a file to request position data from the API and create a Kafka topic. Then, stream the data to a Kafka cluster.

The second is a file to read or consume the topic, it is a Spark Structured Streaming application. The script contains steps from subscribing the Kafka topic, transforming the data, to saving them into files. 

**Update:**

I made modifications for the Kafka Producer script. It can be accessed in the folder named [producer](/producer). The main script is `main.py` which will import `producer.py`. I added some functionalities so the script can receive an argument to specify how long the stream will run for certain time. The arguments are:
- `-o` or `--orbit` to specify how many orbits the stream will fetch from the API. I set one orbit to take 95 minutes, though it is actually around 90-93 minutes.
- `-m` or `--minutes` to specify the stream explicitly runs for certain minutes.
- `-h` or `--help` is a default argument to see the description about the program and how to use it.

> In 24 hours, the ISS can orbit about 16 times, depending on the altitude and gravitational forces. More on this, click the [link](https://spotthestation.nasa.gov/tracking_map.cfm).

Example usage:

1. `python3 main.py -o 2` or `python3 main.py --orbit 2` to fetch two orbits of data. It will run for 190 minutes.
2. `python3 main.py -m 5` or `python3 main.py --minutes 5` to exactly stream the data for five minutes.


## Steps to execute the program

### Preparation

Open a terminal, move to the Kafka folder (e.g. `~/kafka/`), and run the Zookeeper cluster by typing the command

`zookeeper-server-start.sh config/zookeeper.properties`

This will start a Zookeeper service listening on port 2181 as written in the default Zookeeper config file.

Open another terminal and run the Kafka server also with default properties.

`kafka-server-start.sh config/server.properties`

### Running the producer

To run the producer without any argument, follow this step.

Run the simple Kafka Producer, that is the script which creates topic and data streams continuously. Open another terminal and change the directory to where the file is located. Type the following command.

`python3 simple_kafka_producer.py`

To run the producer with a configurable argument, please run

`python3 producer/main.py --orbit 2`

For example, the argument is `--orbit 2` so the stream will go for 190 minutes. Running the script without any argument will stream the data continuously, just like the former script.

#### Optional

To check if the producer runs and creates the topic, run the Kafka Consumer in a separate terminal by typing this following command

`kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic iss-location --from-beginning`

It should be printing the same data produced by the Kafka Producer. Additionally, you can list the available topics by typing

`kafka-topics.sh --bootstrap-server=localhost:9092 --list`

This will print `iss-location` in the shell.

### Save the output

Until this step you have successfully streaming the data to the cluster. The last step is how to get the data from the cluster and save it into files.

Run the Spark Structured Streaming application using `spark-submit`. We need a package to run Kafka, so by typing this command

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 write_output.py`

will run the application properly. The CSV files will be created when the application starts to read the stream.


## Verify the data

Check to the destination folder (mine is `/home/thomas/iss-output`) to verify that CSV files are created and added every one minute (as the `processingTime` parameter I set in the script). 

![list-of-csv-files](/img/list-of-csv-files.png)

Then look into one non-empty file. It should show three columns which are `local_time`, `longitude`, and `latitude`, respectively.

![csv-file](/img/csv-file.png)


## Conclusion

By doing this project, I learned about:
- requesting data from an API,
- creating a program to stream real-time ISS position data using Kafka Producer,
- running a Spark Structured Streaming application to subscribe to a Kafka topic, transform the data received, and save them into CSV files.


## Next Task

I will continue the project by providing a simple visualization of the ISS position.
