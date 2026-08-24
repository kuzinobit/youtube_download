# YouTube Downloader

Программа для скачивания видео с YouTube с помощью `yt-dlp`.

## Установка

Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/kuzinobit/youtube_download
cd youtube_download
```

Создайте виртуальное окружение:

```bash
python3 -m venv .venv
```

Активируйте его.

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```powershell
.venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## FFmpeg

Для объединения видео и аудио программе нужен готовый исполняемый файл FFmpeg.

> Не скачивайте архив с исходным кодом `ffmpeg-*.tar.xz`. Внутри него находятся файлы `.c`, `.h` и исходный код. Нужна готовая скомпилированная сборка.

### Windows

Скачайте готовую **Release Essentials** сборку:

https://www.gyan.dev/ffmpeg/builds/

Распакуйте архив и скопируйте:

```text
bin/ffmpeg.exe
```

в:

```text
ffmpeg/bin/ffmpeg.exe
```

### macOS

Проверьте архитектуру Mac:

```bash
uname -m
```

- `arm64` — Apple Silicon
- `x86_64` — Intel

Скачайте **Release Build → FFmpeg (ZIP)** для своей архитектуры:

https://ffmpeg.martin-riedl.de/

После распаковки скопируйте файл:

```text
ffmpeg
```

в:

```text
ffmpeg/bin/ffmpeg
```

Разрешите выполнение файла:

```bash
chmod +x ffmpeg/bin/ffmpeg
```

Проверка:

```bash
./ffmpeg/bin/ffmpeg -version
```

### Linux

Скачайте **Release Build → FFmpeg (ZIP)** для `amd64` или `arm64`:

https://ffmpeg.martin-riedl.de/

Поместите файл в:

```text
ffmpeg/bin/ffmpeg
```

и разрешите выполнение:

```bash
chmod +x ffmpeg/bin/ffmpeg
```

## Настройка `config.ini`

Сейчас программа использует параметр `video.format`.

Пример:

```ini
[video]
format = bestvideo+bestaudio/best
```

Варианты:

```ini
# Лучшее доступное видео
format = best
```

```ini
# Лучшее видео + лучшее аудио
format = bestvideo+bestaudio/best
```

```ini
# Максимум 1080p
format = bestvideo[height<=1080]+bestaudio/best[height<=1080]
```

```ini
# Максимум 720p
format = bestvideo[height<=720]+bestaudio/best[height<=720]
```

## Запуск

Активируйте виртуальное окружение и выполните:

```bash
python main.py
```

После запуска вставьте ссылку на YouTube:

```text
Введите ссылку на видео YouTube:
```

Пример:

```text
https://www.youtube.com/watch?v=XXXXXXXXXXX
```


Статья на ДЗЕН:
https://dzen.ru/a/Zx-Bc5-ojxdJUm9X
