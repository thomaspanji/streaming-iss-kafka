import json
import requests
from time import sleep
from datetime import datetime
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=['localhost','9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


def get_data():
    res = requests.get('http://api.open-notify.org/iss-now.json')
    data = json.loads(res.content.decode('utf-8'))
    print(data)
    producer.send('iss-location', value=data)
    producer.flush()


def run(args_minutes=None):
    if args_minutes == 1:
        print(f'Streaming for one minute.')
    elif args_minutes is not None:
        print(f'Streaming for {args_minutes} minutes.')

    start_time = datetime.now()

    while True:
        get_data()
        now = datetime.now()
        delta = now - start_time
        minutes_elapsed = delta.total_seconds() / 60
        
        if args_minutes is not None:
            if minutes_elapsed >= args_minutes:
                break
        sleep(10)
        
    sleep(1)
    print('Streaming data finished.')