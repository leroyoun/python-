aqi = int(input("请输入 AQI 数值: "))

if aqi < 0:
    print("输入错误！AQI 不能为负数")
elif aqi <= 50:
    print("一级 (优): 空气清新，极适宜户外活动")
elif aqi <= 100:
    print("二级 (良): 空气质量可接受，可正常活动")
elif aqi <= 150:
    print("三级 (轻度污染): 敏感人群减少户外活动")
elif aqi <= 200:
    print("四级 (中度污染): 敏感人群避免剧烈运动")
elif aqi <= 300:
    print("五级 (重度污染): 所有人适当减少户外活动")
else:
    print("六级 (严重污染): 尽量停留在室内")
