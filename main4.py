from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup
import cv2
import os
import multiprocessing
import pandas as pd
import folium
import concurrent.futures
import time

# 設定初始時間及計數器
count = 0
start_time = time.time()


# 設定thread_process
def process_video(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    img_tag = soup.find("img")
    img_src = img_tag["src"]

    print(f"Processing video from {url}")

    cap = cv2.VideoCapture(img_src)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(f"output_{url[-3:]}.avi", fourcc, 10.0, (432, 240))

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


# input your ID and key

app_id = 'D1063100-c5376cac-eadc-4bac'
app_key = '5c8bfe6d-4155-4f15-b2d0-e69a1a49b44a'

# 認證的url
auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

# 查詢的url
url = " https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/CCTV/City/Taichung"


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

    video_urls = [cctv['VideoStreamURL'] for cctv in data_json['CCTVs'] if "惠中路" in cctv.get('RoadName', '')]

    print(video_urls)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_video, video_urls)

    print("All videos processing complete.")

    # response = requests.get(video_urls[0])
    # soup = BeautifulSoup(response.content, "html.parser")
    # img_tag = soup.find("img")
    # img_src = img_tag["src"]
    # print(img_src)
    #
    # cap = cv2.VideoCapture(img_src)
    #
    # fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # out = cv2.VideoWriter("output.avi", fourcc, 10.0, (432, 240))
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
    '''下面是地圖搜尋器製作'''

    # video_urls = [cctv['VideoStreamURL'] for cctv in data_json['CCTVs']]

    # coordinates_and_roadname = [(cctv['PositionLat'], cctv['PositionLon'], cctv.get('RoadName', '')) for cctv in
    #                             data_json.get('CCTVs', [])]
    # map_center = coordinates_and_roadname[0][:2] if coordinates_and_roadname else [0,
    #                                                                                0]
    # my_map = folium.Map(location=map_center, zoom_start=15)

    # Add markers for each coordinate with RoadName as label
    # for lat, lon, roadname in coordinates_and_roadname:
    #     folium.Marker(location=(lat, lon), popup=roadname + str(lat) + " " + str(lon)).add_to(my_map)
    #
    # # Save the map as an HTML file
    # # my_map.save("PingtungCounty.html")
    # # print(coordinates)

    '''
    121.27843 24.89185
    121.27827 24.89156
    121.27835 24.89189

    '''

    # RoadDirection = [cctv.get('RoadDirection', 'N/A') for cctv in data_json.get('CCTVs', [])]
    # ID = [cctv['CCTVID'] for cctv in data_json['CCTVs']]

    # for url in video_urls:
    #     print(url)
    # for road in RoadName:
    #     print(road)
    # for Direction in RoadDirection:
    #     print(Direction)
    # for cctv_id in ID:
    #     print(cctv_id)
    #
    # df = pd.DataFrame({'cctv_ID': ID, 'Direction': RoadDirection, 'RoadName': RoadName, 'VideoStreamURL': video_urls})

    # 保存为 CSV 文件
    # df.to_csv('Taoyuan.csv', index=False)
    # print("count :", count)
    #
    # start_time = time.time()
    #
    # url = video_urls[0]
    # print(url)
