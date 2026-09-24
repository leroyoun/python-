RATE1 = 0.5283  # 0~230度
RATE2 = 0.5783  # 230~400度
RATE3 = 0.8283  # 400度以上(差额部分)

LEVEL1 = 230
LEVEL2 = 400


def main():
    x = float(input("请输入居民月用电量 (度): "))

    if x <= LEVEL1:
        cost = RATE1 * x
    elif x <= LEVEL2:
        cost = LEVEL1 * RATE1 + (x - LEVEL1) * RATE2
    else:
        cost = LEVEL1 * RATE1 + (LEVEL2 - LEVEL1) * RATE2 + (x - LEVEL2) * RATE3

    print(f"月用电量 {x:g} 度，应缴总电费: {cost:.2f} 元")


if __name__ == "__main__":
    main()