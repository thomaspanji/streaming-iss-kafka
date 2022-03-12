import json
import requests
import datetime
from kafka import KafkaProducer
from time import sleep


ORBIT_MINUTE = 95

producer = KafkaProducer(
    bootstrap_servers=['localhost','9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Get only 20 position data
# for _ in range(20):
#     res = requests.get('http://api.open-notify.org/iss-now.json')
#     data = json.loads(res.content.decode('utf-8'))
#     print(data)
#     producer.send('iss-location', value=data)
#     producer.flush()
#     sleep(10)\

# Non-stop process
# while True:
#     res = requests.get('http://api.open-notify.org/iss-now.json')
#     data = json.loads(res.content.decode('utf-8'))
#     print(data)
#     producer.send('iss-location', value=data)
#     producer.flush()
#     sleep(10)

def get_data():
    res = requests.get('http://api.open-notify.org/iss-now.json')
    data = json.loads(res.content.decode('utf-8'))
    print(data)
    producer.send('iss-location', value=data)
    producer.flush()

start_time = datetime.datetime.now()

while True:
    get_data()
    now = datetime.datetime.now()
    delta = now - start_time
    minutes_elapsed = delta.total_seconds() / 60
    
    if minutes_elapsed >= ORBIT_MINUTE:
        break
    sleep(10)

print('Streaming data finished.')