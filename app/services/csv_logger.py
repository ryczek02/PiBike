import csv
from datetime import datetime
import os
import pytz
from app.config import CONFIG 

timezone = pytz.timezone(CONFIG["TIMEZONE"])
start_time = datetime.now(timezone).strftime('%Y-%m-%d_%H-%M-%S')
csv_filepath = os.path.join(os.getcwd(), f"logs/sensor_log_{start_time}.csv")

with open(csv_filepath, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'gyro_x', 'gyro_y', 'gyro_z', 'accel_x', 'accel_y', 'accel_z', 'gps_lat', 'gps_lon', 'gps_time'])

def log_to_csv(data):
    with open(csv_filepath, 'a', newline='') as file:
        writer = csv.writer(file)
        row = [datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')]
        row += [data.get(k, None) for k in ['gyro_x','gyro_y','gyro_z','accel_x','accel_y','accel_z','gps_lat','gps_lon','gps_time']]
        writer.writerow(row)
