x = float(input("请输入 x 的值: "))
 
# 解法 A: 嵌套分支结构
if x < 10:
    if x <= 1:
        y = x
    else:
        y = 2 * x - 1
else:
    y = 3 * x - 11
 
# 解法 B: elif 扁平化重构 (推荐)
# if x <= 1:
#     y = x
# elif x < 10:
#     y = 2 * x - 1
# else:
#     y = 3 * x - 11
 
print(f"f({x:g}) = {y:g}")

