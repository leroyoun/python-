def main():
    a = float(input("请输入数值 a: "))
    b = float(input("请输入数值 b: "))

    max1 = a if a > b else b
    print(f"三元表达式较大值: {max1}")

    max2 = a
    if b > max2:
        max2 = b
    print(f"预设法  较大值: {max2}")

    if a > b:
        max3 = a
    else:
        max3 = b
    print(f"双分支  较大值: {max3}")

    max4 = max(a, b)
    print(f"max 函数较大值: {max4}")


if __name__ == "__main__":
    main()