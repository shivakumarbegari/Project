from __future__ import print_function
import argparse

from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import datetime
import random
import time
import psutil
from datetime import datetime

USER = 'root'
PASSWORD = 'root'
DBNAME = 'pythonDb'


def main(host='localhost', port=8086):

    
    metric = "cpu"

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    print("Create database: " + DBNAME)
    try:
        client.create_database(DBNAME)
    except InfluxDBClientError:
        # Drop and create
        client.drop_database(DBNAME)
        client.create_database(DBNAME)

    i=1
    while(1):
        #print("loop inside")
        value = psutil.cpu_percent(0.5)
        print("after value ",(i),(value))
        hostName = "shivakumarHP"
        
        json_body = [
        {
            "measurement": "cpu",
            "tags": {
                "host": hostName,
            },
            "fields": {
                'percent': value,
            }
        }
        ]
        client.write_points(json_body)
        i=i+1
        

def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port influxdb http API')
    parser.add_argument('--nb_day', type=int, required=False, default=15,
                        help='number of days to generate time series data')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)