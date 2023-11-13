import requests
from bs4 import BeautifulSoup
import cv2
import os
import multiprocessing
import pandas as pd

# read data

csv_filename = "Taichung.csv"

data = pd.read_csv(csv_filename, skiprows=1)

column_4_data = data.iloc[:, 4]

# process

output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

url = "https://e-traffic.taichung.gov.tw/ATIS_TCC/Device/Showcctv?id=C000001"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
img_tag = soup.find("img")
img_src = img_tag["src"]

cap = cv2.VideoCapture(img_src)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (432, 240))

while True:
    # 擷取影格
    ret, frame = cap.read()
    if ret:
        # 寫入
        out.write(frame)
        # 顯示
        cv2.imshow("CCTV Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

