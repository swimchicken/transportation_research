import folium

# 初始化地圖，指定初始中心座標和縮放級別
map_center = [24.85636, 121.2196]  # 使用提供的座標
my_map = folium.Map(location=map_center, zoom_start=15)

# 第一個點

# 121.27843 24.89185
#     121.27827 24.89156
#     121.27835 24.89189


marker_location1 = [24.89185, 121.27843]
marker_label1 = "中正路 - Point 1"
folium.Marker(location=marker_location1, popup=marker_label1).add_to(my_map)

# 第二個點
marker_location2 = [24.89156, 121.27827]
marker_label2 = "中正路 - Point 2"
folium.Marker(location=marker_location2, popup=marker_label2).add_to(my_map)

# 第三個點
marker_location3 = [24.89189, 121.27835]
marker_label3 = "中正路 - Point 3"
folium.Marker(location=marker_location3, popup=marker_label3).add_to(my_map)

# marker_location4 = [24.98991, 121.28869]
# marker_label4 = "中正路 - Point 4"
# folium.Marker(location=marker_location4, popup=marker_label4).add_to(my_map)
#
# marker_location5 = [24.90691, 121.1456]
# marker_label5 = "中正路 - Point 5"
# folium.Marker(location=marker_location5, popup=marker_label5).add_to(my_map)

# 將地圖儲存為HTML文件
my_map.save("map_with_multiple_markers.html")