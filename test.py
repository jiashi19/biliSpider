from faker import Faker

fake = Faker()
for _ in range(5):  # 生成5个随机UA
    print(fake.user_agent())