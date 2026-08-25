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

    video_format = config.get(
        "video",
        "format",
        fallback="best"
    )

    subtitles_enabled = config.getboolean(
        "subtitles",
        "enabled",
        fallback=False
    )

    subtitles_mode = config.get(
        "subtitles",
        "mode",
        fallback="auto"
    ).lower()

    subtitles_languages = config.get(
        "subtitles",
        "languages",
        fallback="ru"
    )

    subtitles_format = config.get(
        "subtitles",
        "format",
        fallback="srt"
    )

    if subtitles_languages.strip().lower() == "all":
        subtitle_langs = ["all"]
    else:
        subtitle_langs = [
            lang.strip()
            for lang in subtitles_languages.split(",")
            if lang.strip()
        ]

    # FFmpeg
    ffmpeg_file = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"

    ffmpeg_path = os.path.abspath(
        os.path.join("ffmpeg", "bin", ffmpeg_file)
    )

    if not os.path.isfile(ffmpeg_path):
        raise FileNotFoundError(
            f"FFmpeg не найден: {ffmpeg_path}"
        )

    # Каталог для скачанных видео
    output_dir = os.path.abspath("video")
    os.makedirs(output_dir, exist_ok=True)

    # Структура:
    # video/
    # └── Название видео/
    #     ├── Название видео.mp4
    #     └── Название видео.ru.srt
    output_template = os.path.join(
        output_dir,
        "%(title)s",
        "%(title)s.%(ext)s"
    )

    ydl_opts = {
        'format': video_format,
        'merge_output_format': 'mp4',
        'outtmpl': output_template,
        'progress_hooks': [progress_hook],
        'socket_timeout': 60,
        'retries': 5,
        'nocheckcertificates': True,
        'ffmpeg_location': ffmpeg_path,
        'ignoreerrors': True,
    }

    if subtitles_enabled:
        ydl_opts['subtitleslangs'] = subtitle_langs
        ydl_opts['subtitlesformat'] = subtitles_format

        if subtitles_mode == "manual":
            ydl_opts['writesubtitles'] = True

        elif subtitles_mode == "auto":
            ydl_opts['writeautomaticsub'] = True

        elif subtitles_mode == "both":
            ydl_opts['writesubtitles'] = True
            ydl_opts['writeautomaticsub'] = True

        else:
            raise ValueError(
                "Некорректный subtitles.mode. "
                "Допустимые значения: manual, auto, both"
            )

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    url = input("Введите ссылку на видео YouTube: ")
    download_video(url)