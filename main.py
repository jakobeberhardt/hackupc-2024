from pymongo import MongoClient
import os
import datetime

MONGO_CONN_STRING = '127.0.0.1:27017'

print(f'connecting to {MONGO_CONN_STRING}')
client = MongoClient(MONGO_CONN_STRING)

# Our database and collection are both called "workplace"
db = client.metrics
collection = db.create_collection('metrics', timeseries={
  'timeField': 'timestamp',
  'metaField': 'metadata',
  'granularity': 'seconds'
})

# warning: this method modifies the passed `metrics` object
def upload(metrics):
  time = datetime.now() # todo: utcnow?
  count = len(metrics.keys())
  print(f'[{time}] uploading {count} metrics')
  metrics['metadata'] = {}
  metrics['timestamp'] = time
  collection.insert_one(metrics)

upload({
  'temperature': 42.0
})
