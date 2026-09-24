def main():
    aqi = int(input("请输入空气质量指数 AQI (整数): "))

    if aqi <= 50:
        level = "优"
    elif aqi <= 100:
        level = "良"
    elif aqi <= 150:
        level = "轻度污染"
    elif aqi <= 200:
        level = "中度污染"
    elif aqi <= 300:
        level = "重度污染"
    else:
        level = "严重污染"

    print(f"AQI = {aqi}，空气质量级别: {level}")


if __name__ == "__main__":
    main()