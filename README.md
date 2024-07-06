# biliSpider 哔哩哔哩网站爬虫

## 项目简介

biliSpider：基于b站API接口实现的b站内容爬虫，整体基于scrapy框架编写，项目结构参考[scrapy](scrapy-16.readthedocs.io)。

**实现的功能如下**：

- 爬取文章信息(biliSpider/spiders/articleInfo.py)
- 根据关键字搜索相关文章(biliSpider/spiders/articleList.py)
- 爬取评论信息，包括一级评论和二级评论(biliSpider/spiders/commentInfo.py)
- 爬取最新的视频列表，此不包含下载视频(biliSpider/spiders/newVideoInfo.py)
- 爬取用户信息(biliSpider/spiders/userInfo.py)
- 根据关键字搜索用户(biliSpider/spiders/userList.py)
- 根据up主爬取其发布的视频(biliSpider/spiders/VidsByUp.py)
- 下载b站视频(utils/videoscrapy.py)
- wbi鉴权（utils/getSignedParam.py）

## 项目的依赖项

**FFmpeg**：一个开源的软件项目，用于处理多媒体数据（音频、视频等）。

在本项目中，用于将视频下载到本地时对音频流和视频流进行合成，于utils/videoscrapy.py中使用。

该开源工具下载后需配置到环境变量中，下载及环境变量配置教程参考blog：https://blog.csdn.net/qq_45956730/article/details/125272407



## 安装和配置

**安装scrapy库**

```bash
pip install scrapy 
```
**安装bilibili-api-python**

```bash
pip install bilibili-api-python
```

注：若直接install bilibili_api所得到的库不符合该项目使用。

**下载并配置好ffmpeg**

如果无下载视频需求请忽略

**安装并运行redis**

本项目以redis的默认设置进行连接（localhost:6379，db=1）

**更新配置（settings.py）**

```python
#scrapy框架自带，调整并发爬取数量和爬取间隔
CONCURRENT_REQUESTS = 8

DOWNLOAD_DELAY = 0.2
```

```python
#scrapy 下载器中间件，在该处启用
# 代理ip中间件默认未启用，需配合对应代理池程序进行使用（https://github.com/jhao104/proxy_pool）
DOWNLOADER_MIDDLEWARES = {
	# "biliSpider.middlewares.MyproxyMiddleware":544,
    "biliSpider.middlewares.BilispiderDownloaderMiddleware": 543,
}
```

```python
#scrapy 管道处理方法，对应pipelines.py中的管道类
ITEM_PIPELINES = {
    #数据处理pipeline
    "biliSpider.pipelines.DataProcessingPipeline": 300, 
    #数据存储pipeline
    "biliSpider.pipelines.CommentJsonWriterPipeline": 302,
    "biliSpider.pipelines.UserInfoJsonWriterPipeline": 303,
    "biliSpider.pipelines.NewVideoJsonWriterPipeline": 304,
    "biliSpider.pipelines.UserListJsonWriterPipeline": 305,
    "biliSpider.pipelines.ArticleListJsonWriterPipeline":306
}
```

```python
# 日志等级,warning级别只会输出警告信息
LOG_LEVEL = 'WARNING'

# redis中存放视频id的set
VIDEO_ID_SET = "video_id_set"
# 自定义的user agent list
FAKE_UA_LIST = [
    "Opera/8.15.(Windows NT 11.0; fi-FI) Presto/2.9.179 Version/11.00",
    "Mozilla/5.0 (Windows; U; Windows 98) AppleWebKit/535.47.2 (KHTML, like Gecko) Version/4.0.1 Safari/535.47.2",
    "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_9_3 rv:4.0; ce-RU) AppleWebKit/535.15.5 (KHTML, like Gecko) Version/4.0.1 Safari/535.15.5",
    "Mozilla/5.0 (compatible; MSIE 5.0; Windows 98; Win 9x 4.90; Trident/3.0)",
    "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.2; Trident/5.0)"
]
#填充上cookie中的SESSDATA值
COOKIE_SESSDATA_LIST = [
    "sessdata1",
    "sessdata2"
]
```

如涉及到爬取视频，还需要配置utils/videoscrapy.py中的对应cookie值。（**to be improved**）

```python
SESSDATA = "sessdata"
BILI_JCT = "bili_jct"
BUVID3 = "buvid3"
```

## 如何运行项目

```bash
#集成的一体化程序，根据up主id爬取其信息以及其发布的视频（视频文件及评论）
python start.py 
#scrapy 原生命令
scrapy crawl spiderName
```

## 项目的使用示例

```bash
python start.py 
```



```bash
scrapy crawl userInfo -a mid=19642758
#2024-06-24 16:22:07 [userInfo] WARNING: 已访问网页获取数据: userInfo
#2024-06-24 16:22:08 [root] WARNING: 爬取到用户 19642758 的信息
```

## 数据结果

- 数据结构参照items.py
- 数据存储参照pipelines.py
- 爬取结果存放于result文件夹下