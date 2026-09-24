language, math, english, science = input("请输入语文，数学，英语和科学百分制成绩:").split(" ")

language = int(language)
math = int(math)
english = int(english)
science = int(science)

total = language + math + english + science

if total >= 380 and language >= 95 and math >= 95 and english >= 95 and science >= 95:
    print("该生是学优生.")
else:
    print("该生不是学优生.")
