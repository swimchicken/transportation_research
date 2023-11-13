from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)


driver.get("https://tcnvr5.taichung.gov.tw:7001/media/F8-4D-FC-B9-D0-00.mpjpeg?resolution=240p&auth"
           "=cHVibGljdmlld2VyOjYwOTgwMTJhNmY3NjA6MjJhZmY5OWE5YjhhZmYyOTYwYmNmNGEwZDFjMGY0Y2U")  # 使用瀏覽器訪問網頁
img_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.TAG_NAME, "img"))
)

img_src = img_element.get_attribute("src")

# 使用OpenCV下載圖片
image = cv2.imread(img_src)
height, width, layers = image.shape
size = (width,height)
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

# 寫入影片幀
out.write(image)

# 關閉瀏覽器和影片輸出
driver.quit()
out.release()