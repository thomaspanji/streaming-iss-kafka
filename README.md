# streaming-iss-kafka

## Scope of work

This project aims to consume real-time International Space Station (ISS) position data from [this link](http://api.open-notify.org/iss-now.json) and save the data into CSV format files.

I use Apache Kafka to stream the data and leverage the Kafka Producer API for Python. The documentation and how to install this API is available [here](https://kafka-python.readthedocs.io/en/master/). The data received will be proccessed immediately using Spark application and store it in local computer file system.


## Script

This is a raw look when opening the link in the browser. The data is a nested JSON formatted.
![raw-look](/img/raw-json.png)

I created two main Python files. The first is a file to create a topic and get the data like showed in the image above. Then, streams it to a Kafka cluster.

The second is a file to read or consume the topic. I did some transformation before saved the processed data into CSV files.

**Update:**

I made modification for Kafka producer. The script is now can receive an argument to specify how long the stream will run for certain time. The arguments are:
- `-o` or `--orbit` to specify how many orbits the stream will fetch from the API. I set an orbit take for 95 minutes, though actually around 90-93 minutes.
- `-m` or `--minutes` to specify the stream explicitly runs for certain minutes.
- `-h` or `--help` is a default argument to see description about the script and how to use it.

> In the range of 24 hours, the ISS can orbit for about 16 times, depends on the altitude and gravitational forces.


## Steps to run

Open a terminal, change to Kafka bin folder installation (e.g. `kafka/bin/`), and run the Zookeeper cluster by typing the command

`zookeeper-server-start.sh ../config/zookeeper.properties`

This will start a Zookeeper service listening on port 2181 as written in the default Zookeeper config file.

Then run the Kafka server also with default properties.

`kafka-server-start.sh ../config/server.properties`

Run the Kafka Producer, that is the script which create topic and data streams. Open another terminal and change the directory to where the file is located. Type the following command.

`python3 kafka_producer.py`

To check if the producer run and create the topic, run the Kafka Consumer in a separate terminal and move to bin folder of Kafka installation.

`kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic iss-location --from-beginning`

It should be printing the same data produced by the Kafka Producer. Or, you can just list the available topics by typing

`kafka-topics.sh --bootstrap-server=localhost:9092 --list`

This will print `iss-location` in the shell.

Until this step you have successfully streaming the data to the cluster. The last step is how to get the data from the cluster and save it into files.

Run the Spark Structured Streaming application using `spark-submit`. We need a package to run Kafka, so by typing this command

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 write_output.py`

will run the application properly. The CSV files will be created when the application read the stream continuously.


## Verify the data

Check to the destination folder (mine is `/home/thomas/iss-output`) to verify that CSV files are created and added every one minute (as the `processingTime` parameter I set in the script). 

![list-of-csv-files](/img/list-of-csv-files.png)

Then look into the one non-empty file. It should show three columns which are `local_time`,`longitude`, and `latitude`, respectively.

![csv-file](/img/csv-file.png)


## Conclusion

By doing this project, I learned about:
- creating a program to stream real-time ISS position data using Kafka Producer,
- requesting data from API,
- running a Spark Structured Streaming application to subscribe to a Kafka topic, transform the data received, and save them into CSV files.


## Next Task

I will continue the project by providing a simple visualization of the ISS position.
