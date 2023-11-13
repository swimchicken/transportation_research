import concurrent.futures
import requests
from bs4 import BeautifulSoup
import cv2
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import threading

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def process_url(url, output_folder):
    service = Service(executable_path=r'C:\Users\user\chromedriver-win64\chromedriver-win64\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)  # 使用瀏覽器訪問網頁
    img_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "img"))
    )

    # 獲取影像的src屬性
    img_src = img_element.get_attribute("src")
    print(img_src)

    cap = cv2.VideoCapture(img_src)
    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            driver.refresh()  # 重新載入網頁
            img_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
            # 獲取影像的src屬性
            img_src = img_element.get_attribute("src")
            print("無法讀取影格")
            print(img_src)

            cap = cv2.VideoCapture(img_src)  # 更新影像的src屬性
            continue  # 跳過本次循環，重新讀取影格

        frame_count += 1
        frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_filename, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1)  # 在每次請求之後休眠1秒

    cap.release()
    cv2.destroyAllWindows()

    # 將處理結果儲存到檔案
    output_file = os.path.join(output_folder, "output.txt")
    with open(output_file, "w") as f:
        f.write(img_src)

    driver.quit()  # 关闭WebDriver实例


if __name__ == '__main__':
    start_index = 0  # 起始索引
    end_index = 15  # 結束索引（不包含）

    csv_filename = "Taichung.csv"
    data = pd.read_csv(csv_filename, skiprows=1)
    column_4_data = data.iloc[:, 4]

    output_base_folder = "dataset"
    if not os.path.exists(output_base_folder):
        os.makedirs(output_base_folder)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        counter = 0
        for i in range(start_index, end_index):
            output_folder = os.path.join(output_base_folder, f"output{i}")
            os.makedirs(output_folder, exist_ok=True)
            executor.submit(process_url, column_4_data[i], output_folder)