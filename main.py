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

print(img_src)

cap = cv2.VideoCapture(img_src)

frame_count = 0

while True:
    ret, frame = cap.read()

    cv2.imshow("CCTV Stream", frame)

    frame_count += 1
    frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
    cv2.imwrite(frame_filename, frame)
    print(f"儲存 {frame_filename}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()