import requests
from bs4 import BeautifulSoup
import cv2
import os
import multiprocessing
import pandas as pd

import time

# set time

start_time = time.time()

# read data

# csv_filename = "Taichung.csv"
#
# data = pd.read_csv(csv_filename, skiprows=1)
#
# column_4_data = data.iloc[:, 4]

# process

output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

url = "https://e-traffic.taichung.gov.tw/ATIS_TCC/Device/Showcctv?id=C000001"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
img_tag = soup.find("img")
img_src = img_tag["src"]
print(img_src)

cap = cv2.VideoCapture(img_src)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 10.0, (432, 240))

while True:
    ret, frame = cap.read()
    if ret:
        out.write(frame)
        cv2.imshow("CCTV Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 設定計時器(10 sec)
    if time.time() - start_time >= 3600:
        break
# 'C000299', 'C000172', 'C000291', 'C000160', 'C000387', 'C000015', 'C000008']
