
# from faker import Faker
#
# fake = Faker()
# for _ in range(5):  # 生成5个随机UA
#     print(fake.user_agent())

total_count=120
page=int(total_count / 30) + 1 if total_count%30!=0 else int(total_count / 30)
print(page)