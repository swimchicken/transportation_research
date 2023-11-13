from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup
import cv2
import os
import multiprocessing
import pandas as pd

import time

# 輸入你的金鑰ID and key

app_id = 'D1063100-c5376cac-eadc-4bac'
app_key = '5c8bfe6d-4155-4f15-b2d0-e69a1a49b44a'

count = 0

# 認證的url
auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

# 查詢的url
url = " https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/CCTV/City/Taoyuan"


class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return {
            'content-type': content_type,
            'grant_type': grant_type,
            'client_id': self.app_id,
            'client_secret': self.app_key
        }


class data():

    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')

        return {
            'authorization': 'Bearer ' + access_token
        }


if __name__ == '__main__':
    try:
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())
    except:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())
    print(auth_response)
    pprint(auth_response.text)
    print(data_response)
    pprint(json.loads(data_response.text))
    data_json = json.loads(data_response.text)

    video_urls = [cctv['VideoStreamURL'] for cctv in data_json['CCTVs']]
    RoadName = [cctv.get('RoadName', 'N/A') for cctv in data_json.get('CCTVs', [])]
    RoadDirection = [cctv.get('RoadDirection', 'N/A') for cctv in data_json.get('CCTVs', [])]
    ID = [cctv['CCTVID'] for cctv in data_json['CCTVs']]

    for url in video_urls:
        print(url)
    for road in RoadName:
        print(road)
    for Direction in RoadDirection:
        print(Direction)
    for cctv_id in ID:
        print(cctv_id)

    df = pd.DataFrame({'cctv_ID': ID, 'Direction': RoadDirection, 'RoadName': RoadName, 'VideoStreamURL': video_urls})

    # 保存为 CSV 文件
    df.to_csv('Taoyuan.csv', index=False)
    # print("count :", count)
    #
    # start_time = time.time()
    #
    # url = video_urls[0]
    # print(url)
    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, "html.parser")
    # img_tag = soup.find("img")
    # img_src = img_tag["src"]
    #
    # cap = cv2.VideoCapture(url)
    #
    # fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # out = cv2.VideoWriter("output.avi", fourcc, 10.0, (320, 240))
    #
    # while True:
    #     ret, frame = cap.read()
    #     if ret:
    #         out.write(frame)
    #         cv2.imshow("CCTV Stream", frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    #     # 設定計時器(10 sec)
    #     if time.time() - start_time >= 3600:
    #         break
