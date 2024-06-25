# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleInfoItem(scrapy.Item):
    view = scrapy.Field()  # 阅读数
    favorite = scrapy.Field()  # 收藏数
    like = scrapy.Field()  # 点赞数
    dislike = scrapy.Field()  # 点踩数
    reply = scrapy.Field()  # 评论数
    share = scrapy.Field()  # 分享数
    coin = scrapy.Field()  # 投币数
    dynamic = scrapy.Field()  # 动态转发数

    title = scrapy.Field()  # 标题
    banner_url = scrapy.Field()  # 封面
    mid = scrapy.Field()  # 作者mid
    author_name = scrapy.Field()  # 作者名字
    type = scrapy.Field()  # 专栏分类


class CommentItem(scrapy.Item):
    platform = scrapy.Field()  # 视频平台
    create_date = scrapy.Field()  # 创建日期 （以时间戳存储）
    collect_date = scrapy.Field()  # 爬取日期 （以时间戳存储）
    user_id = scrapy.Field()  # 对应用户id

    user_name = scrapy.Field()  # 用户名
    content = scrapy.Field()  # 评论内容
    likes_count = scrapy.Field()  # 点赞数
    comments_count = scrapy.Field()  # 子评论数量

    is_first_level = scrapy.Field()  # 是否为一级评论
    url = scrapy.Field()  # 视频url
    comment_url = scrapy.Field()  # 当前评论的url
    user_photo = scrapy.Field()  # 用户照片
    parent_content = scrapy.Field()  # 父评论内容（如果本身为父评论，则为0）
    parent_create_date = scrapy.Field()  # 略
    parent_user_id = scrapy.Field()  # 略
    description = scrapy.Field()

    comment_id = scrapy.Field()  # 评论的id
    oid = scrapy.Field()  # 视频or文章的id


class UserInfoItem(scrapy.Item):
    mid = scrapy.Field()  # 用户id
    name = scrapy.Field()  # 用户名称
    sex = scrapy.Field()  # 性别
    user_photo = scrapy.Field()  # 头像
    fans = scrapy.Field()  # 粉丝数
    attention = scrapy.Field()  # 关注数
    sign = scrapy.Field()  # 签名
    level = scrapy.Field()  # 等级
    type = scrapy.Field()  # 认证类型 数字 后期转换后与official_verify合并展示
    official_verify = scrapy.Field()  # 认证
    vip = scrapy.Field()  # vip类型
    like_num = scrapy.Field()  # 获赞数


class VideoItem(scrapy.Item):
    # 定义视频详情字段
    aid = scrapy.Field()  # avid
    tid = scrapy.Field()  # 视频主分区id
    sub_tid = scrapy.Field()  # 视频子分区id
    title = scrapy.Field()  # 视频标题
    description = scrapy.Field()  # 视频简介
    pubdate = scrapy.Field()  # 稿件发布时间（时间戳）
    view = scrapy.Field()  # 播放数
    danmaku = scrapy.Field()  # 弹幕数
    reply = scrapy.Field()  # 评论数
    favorite = scrapy.Field()  # 收藏数
    coin = scrapy.Field()  # 投币数
    share = scrapy.Field()  # 分享数
    like = scrapy.Field()  # 点赞量
    url = scrapy.Field()  # 视频链接
    pic = scrapy.Field()  # 视频封面图片url

    # 定义视频作者详情字段
    owner_mid = scrapy.Field()  # 作者id
    owner_name = scrapy.Field()  # 作者名称
    owner_face = scrapy.Field()  # 作者头像


class UserListItem(scrapy.Item):
    # 定义用户列表字段
    # uname = scrapy.Field()  # 用户名称
    # mid = scrapy.Field()  # 用户id
    result = scrapy.Field()  # 所有数据


class ArticleListItem(scrapy.Item):
    id = scrapy.Field()  # 文章id
    mid = scrapy.Field()  # 用户id
    title = scrapy.Field()  # 标题
