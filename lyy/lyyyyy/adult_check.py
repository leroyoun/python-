from datetime import date


def main():
    birth_year = int(input("请输入出生年份: "))
    current_year = date.today().year
    age = current_year - birth_year

    if age >= 18:
        print("是成年人!")


if __name__ == "__main__":
    main()