from kafka import KafkaProducer
import csv, time, random
import json
from pathlib import Path

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

csv_path = Path(__file__).resolve().parent / '../data/btcusd_1-min_data.csv'

#with open(r'..\data\btcusd_1-min_data.csv', 'r') as file:
with open(csv_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        producer.send('bitcoin-topic', value=row)
        print("Sent:", row)
        #ime.sleep(0.0002)