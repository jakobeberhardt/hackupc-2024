#!/usr/bin/python3
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import serial
import random
import struct
import math

def get_esp_port():
  return serial.Serial('/dev/ttyUSB0', baudrate=9600)

url = os.getenv('INFLUX_URL')
token = os.getenv('INFLUX_TOKEN')
org = os.getenv('INFLUX_ORG')
bucket = os.getenv('INFLUX_BUCKET')
USE_FAKE_DATA = os.getenv('USE_FAKE_DATA') == 'yes'
SHOULD_UPLOAD = url is not None

def get_write_api():
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api()
    return write_api

def upload(write_api, point):
  write_api.write(bucket=bucket, org=org, record=point)

if __name__ == '__main__':
  print('starting up')
  if True:
    random.seed(2024)
  else:
    port = get_esp_port()
  if SHOULD_UPLOAD:
    write_api = get_write_api()

  while True:
    if True:
      temp = random.uniform(22, 24)
      humidity = random.uniform(40, 50)
      sound = random.uniform(0, 255)
    else:
      measurement_bytes = port.read(12)
      temp, humidity, sound = struct.unpack('fff', measurement_bytes)# little endian
    if math.isnan(temp) or not (-20 < temp < 50) or not (0 < humidity < 100):
      assert(math.isnan(humidity))
      print(f'failed checksum or invalid data (temp={temp}, hum={humidity}, sound={sound}); skipping')
    else:
      print(f'uploading temperature: {temp}ºC, hum {humidity}%, sound {sound}')
      if SHOULD_UPLOAD:
        p = Point('workplace')\
              .field('temperature', temp)\
              .field('humidity', humidity)\
              .field('sound', sound)
        upload(write_api, p)
