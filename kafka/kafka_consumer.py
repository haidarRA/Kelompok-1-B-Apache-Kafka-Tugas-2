from kafka import KafkaConsumer
import json, time
import pandas as pd
from pathlib import Path

data_dir = Path(__file__).resolve().parent / '../data/batch'
data_dir.mkdir(parents=True, exist_ok=True)

consumer = KafkaConsumer('bitcoin-topic', bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

batch = []
batch_size = 2330000
file_index = 1

for message in consumer:
    batch.append(message.value)
    
    if (len(batch) >= batch_size) and (file_index <= 3):
        df = pd.DataFrame(batch)
        output_file = data_dir / f'batch_{file_index}.csv'
        df.to_csv(output_file, index=False)
        print(f'Saved {output_file}')
        batch = []
        file_index += 1