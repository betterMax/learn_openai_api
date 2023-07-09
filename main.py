from Functions.summarize_text import reply_text

# 显示可用的功能
print("请选择一个功能：")
print("1. 爬取并总结网页")
print("2. 其他功能（如果有）")
choice = input("你的选择是：")

# 根据用户的选择执行不同的功能
if choice == "1":
    message = input("请输入一个网页链接：")
    response = reply_text(message)
    print(response)
elif choice == "2":
    print("执行其他功能...")
else:
    print("无效的选择。")