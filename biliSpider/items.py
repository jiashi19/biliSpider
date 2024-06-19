# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleInfoItem(scrapy.Item):
    view = scrapy.Field()
    favorite = scrapy.Field()
    like = scrapy.Field()
    dislike = scrapy.Field()
    reply = scrapy.Field()
    share = scrapy.Field()
    coin = scrapy.Field()
    dynamic = scrapy.Field()  # 动态转发数

    title = scrapy.Field()
    banner_url = scrapy.Field()
    mid = scrapy.Field()
    author_name = scrapy.Field()
    type = scrapy.Field()


class CommentItem(scrapy.Item):
    platform = scrapy.Field() # 视频平台
    create_date = scrapy.Field() # 创建日期 （以时间戳存储）
    collect_date = scrapy.Field() # 爬取日期 （以时间戳存储）
    user_id = scrapy.Field()     # 对应用户id

    user_name = scrapy.Field()   # 用户名
    content = scrapy.Field()     # 评论内容
    likes_count = scrapy.Field() # 点赞数
    comments_count = scrapy.Field() # 子评论数量

    is_first_level = scrapy.Field() # 是否为一级评论
    url = scrapy.Field()    # 视频url
    comment_url = scrapy.Field() # 当前评论的url
    user_photo = scrapy.Field() #用户照片
    parent_content=scrapy.Field() # 父评论内容（如果本身为父评论，则为0）
    parent_create_date = scrapy.Field() # 略
    parent_user_id = scrapy.Field()  # 略
    description = scrapy.Field()

    comment_id=scrapy.Field() # 评论的id
    oid=scrapy.Field()# 视频or文章的id

class UserInfoItem(scrapy.Item):
    mid=scrapy.Field()  #用户id
    name=scrapy.Field() #用户名称
    sex=scrapy.Field()  #性别
    user_photo=scrapy.Field() #头像
    fans=scrapy.Field() # 粉丝数
    attention=scrapy.Field() # 关注数
    sign=scrapy.Field()  #签名
    level=scrapy.Field() # 等级
    type=scrapy.Field() # 认证类型 数字 后期转换后与official_verify合并展示
    official_verify=scrapy.Field() # 认证
    vip=scrapy.Field()             # vip类型
    like_num=scrapy.Field()       # 获赞数
