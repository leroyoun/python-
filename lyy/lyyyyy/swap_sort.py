def main():
    a = int(input("请输入第一个整数 a: "))
    b = int(input("请输入第二个整数 b: "))

    if a > b:
        a, b = b, a

    print(f"升序输出: {a} {b}")


if __name__ == "__main__":
    main()