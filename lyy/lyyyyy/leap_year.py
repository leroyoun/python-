def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


if __name__ == "__main__":
    try:
        year = int(input("请输入一个公历年份："))
        if is_leap_year(year):
            print(f"{year} 年是闰年")
        else:
            print(f"{year} 年是平年")
    except ValueError:
        print("输入有误，请输入一个整数年份")
