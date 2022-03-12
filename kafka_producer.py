import json
import requests
from kafka import KafkaProducer
from time import sleep


producer = KafkaProducer(
    bootstrap_servers=['localhost','9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# for _ in range(20):
#     res = requests.get('http://api.open-notify.org/iss-now.json')
#     data = json.loads(res.content.decode('utf-8'))
#     print(data)
#     producer.send('iss-location', value=data)
#     producer.flush()
#     sleep(10)\

while True:
    res = requests.get('http://api.open-notify.org/iss-now.json')
    data = json.loads(res.content.decode('utf-8'))
    print(data)
    producer.send('iss-location', value=data)
    producer.flush()
    sleep(10)
    