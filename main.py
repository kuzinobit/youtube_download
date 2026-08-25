import os
import sys
import tempfile
import configparser

import yt_dlp


def progress_hook(d):
    if d["status"] == "downloading":
        percentage = d.get("_percent_str", "")
        print(f"Скачивание: {percentage}")


def is_auth_error(error):
    """
    Проверяет, требует ли YouTube авторизацию/cookies.
    """
    text = str(error).lower()

    auth_messages = (
        "sign in to confirm you’re not a bot",
        "sign in to confirm you're not a bot",
        "use --cookies-from-browser or --cookies",
        "login_required",
    )

    return any(message in text for message in auth_messages)


def export_browser_cookies(browser, cookie_file):
    """
    Один раз получает cookies из браузера и сохраняет
    их во временный файл.
    """

    print(
        f"\nYouTube запросил подтверждение. "
        f"Получаем cookies из браузера: {browser}\n"
    )

    options = {
        "cookiesfrombrowser": (browser,),
        "cookiefile": cookie_file,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        # Обращение к cookiejar инициирует загрузку
        # cookies из браузера
        _ = ydl.cookiejar

    # Ограничиваем права на временный файл
    if os.path.isfile(cookie_file):
        try:
            os.chmod(cookie_file, 0o600)
        except OSError:
            pass

    print("Cookies получены.")


def download_video(url):
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")

    # =========================================================
    # VIDEO
    # =========================================================

    video_format = config.get(
        "video",
        "format",
        fallback="best"
    )

    # =========================================================
    # SUBTITLES
    # =========================================================

    subtitles_enabled = config.getboolean(
        "subtitles",
        "enabled",
        fallback=False
    )

    subtitles_mode = config.get(
        "subtitles",
        "mode",
        fallback="auto"
    ).strip().lower()

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

    subtitles_delay = config.getfloat(
        "subtitles",
        "delay",
        fallback=2
    )

    if subtitles_languages.strip().lower() == "all":
        subtitle_langs = ["all"]
    else:
        subtitle_langs = [
            lang.strip()
            for lang in subtitles_languages.split(",")
            if lang.strip()
        ]

    # =========================================================
    # YOUTUBE
    # =========================================================

    cookies_mode = config.get(
        "youtube",
        "cookies",
        fallback="auto"
    ).strip().lower()

    browser = config.get(
        "youtube",
        "browser",
        fallback="chrome"
    ).strip().lower()

    if cookies_mode not in ("auto", "always", "never"):
        raise ValueError(
            "youtube.cookies должен иметь значение: "
            "auto, always или never"
        )

    # =========================================================
    # FFMPEG
    # =========================================================

    ffmpeg_file = (
        "ffmpeg.exe"
        if os.name == "nt"
        else "ffmpeg"
    )

    ffmpeg_path = os.path.abspath(
        os.path.join(
            "ffmpeg",
            "bin",
            ffmpeg_file
        )
    )

    if not os.path.isfile(ffmpeg_path):
        raise FileNotFoundError(
            f"FFmpeg не найден: {ffmpeg_path}"
        )

    # =========================================================
    # OUTPUT
    # =========================================================

    output_dir = os.path.abspath("video")

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_template = os.path.join(
        output_dir,
        "%(title)s",
        "%(title)s.%(ext)s"
    )

    # =========================================================
    # TEMP COOKIES
    # =========================================================

    with tempfile.TemporaryDirectory(
        prefix="youtube_download_"
    ) as temp_dir:

        cookie_file = os.path.join(
            temp_dir,
            "cookies.txt"
        )

        cookies_loaded = False

        def load_cookies():
            nonlocal cookies_loaded

            if cookies_loaded:
                return

            export_browser_cookies(
                browser,
                cookie_file
            )

            cookies_loaded = True

        def execute(options):
            """
            Запускает yt-dlp.

            В режиме auto сначала работает без cookies.
            Cookies используются только при ошибке авторизации.
            """

            run_options = options.copy()

            # Если cookies уже были получены ранее,
            # используем их повторно
            if cookies_loaded:
                run_options["cookiefile"] = cookie_file

            # Режим always
            elif cookies_mode == "always":
                load_cookies()
                run_options["cookiefile"] = cookie_file

            try:
                with yt_dlp.YoutubeDL(run_options) as ydl:
                    ydl.download([url])

                return

            except yt_dlp.utils.DownloadError as error:

                # В режиме auto используем браузер
                # только при запросе авторизации
                if (
                    cookies_mode == "auto"
                    and not cookies_loaded
                    and is_auth_error(error)
                ):
                    load_cookies()

                    retry_options = options.copy()
                    retry_options["cookiefile"] = cookie_file

                    print(
                        "\nПовторяем запрос с cookies...\n"
                    )

                    with yt_dlp.YoutubeDL(
                        retry_options
                    ) as ydl:
                        ydl.download([url])

                    return

                raise

        # =====================================================
        # COMMON OPTIONS
        # =====================================================

        common_opts = {
            "socket_timeout": 60,
            "retries": 5,
            "nocheckcertificates": True,
            "ffmpeg_location": ffmpeg_path,

            "extractor_args": {
                "youtube": {
                    "player_client": [
                        "default",
                        "web_embedded"
                    ]
                }
            },
        }

        # =====================================================
        # DOWNLOAD VIDEO
        # =====================================================

        video_opts = common_opts.copy()

        video_opts.update({
            "format": video_format,
            "merge_output_format": "mp4",
            "outtmpl": output_template,
            "progress_hooks": [progress_hook],
        })

        print("\nСкачивание видео...\n")

        try:
            execute(video_opts)

        except yt_dlp.utils.DownloadError as error:
            print("\nНе удалось скачать видео:")
            print(error)
            return False

        print("\nВидео скачано.\n")

        # =====================================================
        # DOWNLOAD SUBTITLES
        # =====================================================

        if not subtitles_enabled:
            return True

        for language in subtitle_langs:

            print(
                f"\nСкачивание субтитров: "
                f"{language}\n"
            )

            subtitle_opts = common_opts.copy()

            subtitle_opts.update({
                "skip_download": True,
                "outtmpl": output_template,
                "subtitleslangs": [language],
                "subtitlesformat": subtitles_format,

                # Небольшая пауза уменьшает количество
                # быстрых запросов к YouTube
                "sleep_interval_subtitles": subtitles_delay,
            })

            if subtitles_mode == "manual":
                subtitle_opts["writesubtitles"] = True

            elif subtitles_mode == "auto":
                subtitle_opts["writeautomaticsub"] = True

            elif subtitles_mode == "both":
                subtitle_opts["writesubtitles"] = True
                subtitle_opts["writeautomaticsub"] = True

            else:
                raise ValueError(
                    "Некорректный subtitles.mode. "
                    "Допустимые значения: "
                    "manual, auto, both"
                )

            try:
                execute(subtitle_opts)

                print(
                    f"\nСубтитры '{language}' "
                    f"скачаны."
                )

            except yt_dlp.utils.DownloadError as error:

                error_text = str(error)

                if "429" in error_text:
                    print(
                        f"\nСубтитры '{language}' "
                        f"не скачаны."
                    )
                    print(
                        "YouTube вернул HTTP 429 "
                        "Too Many Requests."
                    )
                    print(
                        "Видео и остальные субтитры "
                        "сохраняются."
                    )

                else:
                    print(
                        f"\nНе удалось скачать "
                        f"субтитры '{language}':"
                    )
                    print(error)

        return True


if __name__ == "__main__":
    url = input(
        "Введите ссылку на видео YouTube: "
    )

    try:
        success = download_video(url)

    except FileNotFoundError as error:
        print(error)
        success = False

    except ValueError as error:
        print(error)
        success = False

    sys.exit(0 if success else 1)