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
    platform = scrapy.Field()
    create_date = scrapy.Field()
    collect_date = scrapy.Field()
    user_id = scrapy.Field()

    user_name = scrapy.Field()
    content = scrapy.Field()
    likes_count = scrapy.Field()
    comments_count = scrapy.Field()

    is_first_level = scrapy.Field()
    url = scrapy.Field()
    comment_url = scrapy.Field()
    user_photo = scrapy.Field()
    parent_content=scrapy.Field()
    parent_create_date = scrapy.Field()
    parent_user_id = scrapy.Field()
    description = scrapy.Field()

    reqNo=scrapy.Field()

