from datetime import date, datetime


def main():
    today = date.today()
    print(f"当前系统日期: {today.strftime('%Y-%m-%d')}")

    while True:
        text = input("请输入目标交付日期 (格式: 年-月-日，例如 2026-12-31): ").strip()
        try:
            target = datetime.strptime(text, "%Y-%m-%d").date()
            break
        except ValueError:
            print("日期格式不正确，请按 年-月-日 格式输入，例如 2026-12-31。")

    diff = (target - today).days

    if diff > 0:
        print(f"距离目标交付日期 {target.strftime('%Y-%m-%d')} 还剩 {diff} 天。")
    elif diff == 0:
        print(f"目标交付日期 {target.strftime('%Y-%m-%d')} 就是今天，请尽快交付！")
    else:
        print(f"目标交付日期 {target.strftime('%Y-%m-%d')} 已过期 {-diff} 天。")


if __name__ == "__main__":
    main()