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

csv_filename = "Taichung.csv"

data = pd.read_csv(csv_filename, skiprows=1)

column_4_data = data.iloc[:, 4]

# process

output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

url = "http://61.60.38.53:8601/Interface/Cameras/GetJPEGStream?Camera=CCTV006&Width=320&Height=240&Quality=70&FPS=10&AuthUser=web"


# response = requests.get(url, verify=False)
# soup = BeautifulSoup(response.content, "html.parser")
# img_tag = soup.find("img")
# img_src = img_tag["src"]
# print(img_src)

cap = cv2.VideoCapture(url)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 10.0, (320, 240))

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
