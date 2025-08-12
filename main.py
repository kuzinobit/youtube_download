import yt_dlp
import os
import configparser

def progress_hook(d):
    if d['status'] == 'downloading':
        percentage = d['_percent_str']
        print(f"Скачивание: {percentage}")

def download_video(url):
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    video_format = config.get("video", "format", fallback="best")

    ffmpeg_path = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
    os.environ["PATH"] += os.pathsep + os.path.abspath(os.path.dirname(ffmpeg_path))

    ydl_opts = {
        # Формат указывается в виде строки, например 'bestvideo+bestaudio/best в config.ini
        'format': video_format,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'socket_timeout': 60,
        'retries': 5,
        'nocheckcertificates': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Введите ссылку на видео YouTube: ")
    download_video(url)