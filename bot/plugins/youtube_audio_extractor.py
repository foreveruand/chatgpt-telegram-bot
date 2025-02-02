import logging
import re
from typing import Dict

import yt_dlp

from .plugin import Plugin


class YouTubeAudioExtractorPlugin(Plugin):
    """
    A plugin to extract audio from a YouTube video
    """

    def get_source_name(self) -> str:
        return "YouTube Audio Extractor"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "extract_youtube_audio",
            "description": "Extract audio from a video from websites like YouTube, bilibili and others",
            "parameters": {
                "type": "object",
                "properties": {
                    "youtube_link": {"type": "string", "description": "video link to extract audio from"}
                },
                "required": ["youtube_link"],
            },
        }]

    async def execute(self, function_name, helper, **kwargs) -> Dict:
        link = kwargs['youtube_link']
        try:
            ydl_opts = {
                'outtmpl': '.cache/%(title)s.%(ext)s',  # 设置输出文件名格式
                'format': 'bestaudio/best',  # 下载最佳质量的视频
                'quiet': True,  # 不显示下载进度
                'embedthumbnail': True,  # 将缩略图嵌入到音频文件中
                'addmetadata': True,  # 将元数据添加到音频文件中
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 提取视频信息
                info_dict = ydl.extract_info(link, download=False)

                # 获取视频的标题和文件名
                title = info_dict.get('title', 'Unknown Title')
                output = ydl.prepare_filename(info_dict)
                ydl.download(link)

            # audio.download(filename=output)
            return {
                'direct_result': {
                    'kind': 'file',
                    'format': 'path',
                    'value': output
                }
            }
        except Exception as e:
            logging.warning(f'Failed to extract audio from YouTube video: {str(e)}')
            return {'result': 'Failed to extract audio'}
