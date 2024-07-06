import asyncio
from bilibili_api import video, Credential, HEADERS
import httpx
import os
import tqdm
SESSDATA = "sessdata"
BILI_JCT = "bili_jct"
BUVID3 = "buvid3"

# FFMPEG 路径，查看：http://ffmpeg.org/
FFMPEG_PATH = "ffmpeg"

# 创建保存视频的文件夹
output_dir = 'result/video'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


async def download_url(url: str, out: str, info: str):
    # 下载函数
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                process += len(chunk)
                # print(f'下载 {info} {process} / {length}')
                f.write(chunk)


async def download_video(bvid: str, credential: Credential):
    # 实例化 Video 类
    v = video.Video(bvid=bvid, credential=credential)
    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams()
    # 有 MP4 流 / FLV 流两种可能
    if detecter.check_flv_stream() == True:
        # FLV 流下载
        flv_temp = os.path.join(output_dir, "flv_temp.flv")
        await download_url(streams[0].url, flv_temp, "FLV 音视频流")
        # 转换文件格式
        output_path = os.path.join(output_dir, f"{bvid}.mp4")
        os.system(f'{FFMPEG_PATH} -i {flv_temp} {output_path}')
        # 删除临时文件
        os.remove(flv_temp)
    else:
        # MP4 流下载
        video_temp = os.path.join(output_dir, "video_temp.m4s")
        audio_temp = os.path.join(output_dir, "audio_temp.m4s")
        await download_url(streams[0].url, video_temp, "视频流")
        await download_url(streams[1].url, audio_temp, "音频流")
        # 混流
        output_path = os.path.join(output_dir, f"{bvid}.mp4")
        os.system(f'{FFMPEG_PATH} -i {video_temp} -i {audio_temp} -vcodec copy -acodec copy {output_path}')
        # 删除临时文件
        os.remove(video_temp)
        os.remove(audio_temp)

    print(f'已下载为：{bvid}.mp4')


async def main(bvid):
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # # 从文件中读取 bvid 列表
    # with open('bvids.txt', 'r') as f:
    #     bvids = [line.strip() for line in f.readlines()]

    # 下载每个 bvid 对应的视频
    await download_video(bvid, credential)


def download_video_by_bvid(bvid):
    asyncio.get_event_loop().run_until_complete(main(bvid))


if __name__ == '__main__':
    bvid="BV17T421k775"

    # 主入口
    asyncio.get_event_loop().run_until_complete(main(bvid))
