def main():
    x = float(input("请输入 x: "))

    if x < 1:
        y = x
    elif x < 10:
        y = 2 * x - 1
    else:
        y = 3 * x - 11

    print(f"f({x:g}) = {y:g}")


if __name__ == "__main__":
    main()