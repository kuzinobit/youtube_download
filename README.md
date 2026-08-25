# YouTube Downloader

Программа для скачивания видео с YouTube с помощью `yt-dlp`.

Поддерживает:

- скачивание видео в выбранном качестве;
- объединение видео и аудио через FFmpeg;
- сохранение каждого видео в отдельную папку;
- скачивание субтитров отдельными файлами;
- ручные и автоматические субтитры;
- использование cookies браузера только при необходимости;
- Windows, macOS и Linux.

## Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/kuzinobit/youtube_download
cd youtube_download
```

Создайте виртуальное окружение:

```bash
python3 -m venv .venv
```

Активируйте его.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Deno

Для корректной работы `yt-dlp` с YouTube требуется JavaScript runtime.

Установка Deno:

https://docs.deno.com/runtime/getting_started/installation/

Проверка:

```bash
deno --version
```

## FFmpeg

FFmpeg используется для объединения видео и аудио.

> Не скачивайте архив с исходным кодом `ffmpeg-*.tar.xz`. Нужна готовая скомпилированная сборка.

### Windows

Скачайте **Release Essentials**:

https://www.gyan.dev/ffmpeg/builds/

Из архива скопируйте:

```text
bin/ffmpeg.exe
```

в:

```text
ffmpeg/bin/ffmpeg.exe
```

### macOS

Проверьте архитектуру:

```bash
uname -m
```

- `arm64` — Apple Silicon
- `x86_64` — Intel

Скачайте **Release Build → FFmpeg (ZIP)** для своей архитектуры:

https://ffmpeg.martin-riedl.de/

Поместите файл:

```text
ffmpeg
```

в:

```text
ffmpeg/bin/ffmpeg
```

Разрешите выполнение:

```bash
chmod +x ffmpeg/bin/ffmpeg
```

Проверка:

```bash
./ffmpeg/bin/ffmpeg -version
```

### Linux

Скачайте готовую сборку FFmpeg для `amd64` или `arm64`:

https://ffmpeg.martin-riedl.de/

Поместите файл в:

```text
ffmpeg/bin/ffmpeg
```

Разрешите выполнение:

```bash
chmod +x ffmpeg/bin/ffmpeg
```

## Настройка `config.ini`

Пример:

```ini
[video]
format = bestvideo+bestaudio/best

[subtitles]
enabled = true
mode = auto
languages = ru,en
format = srt
delay = 2

[youtube]
cookies = auto
browser = chrome
```

### Видео

```ini
[video]
format = bestvideo+bestaudio/best
```

Примеры:

```ini
# Лучшее видео + лучшее аудио
format = bestvideo+bestaudio/best
```

```ini
# Лучший единый формат
format = best
```

```ini
# Максимум 1080p
format = bestvideo[height<=1080]+bestaudio/best[height<=1080]
```

```ini
# Максимум 720p
format = bestvideo[height<=720]+bestaudio/best[height<=720]
```

### Субтитры

```ini
[subtitles]
enabled = true
mode = auto
languages = ru,en
format = srt
delay = 2
```

`enabled` включает или отключает скачивание субтитров.

`mode`:

```text
manual   только субтитры, добавленные автором
auto     автоматические субтитры YouTube
both     ручные и автоматические субтитры
```

Языки перечисляются через запятую:

```ini
languages = ru,en
```

Например, только русский:

```ini
languages = ru
```

Формат субтитров:

```ini
format = srt
```

`delay` задает паузу между запросами субтитров:

```ini
delay = 2
```

Если YouTube возвращает `HTTP 429` для отдельной дорожки субтитров, видео и остальные доступные субтитры сохраняются.

### Cookies браузера

```ini
[youtube]
cookies = auto
browser = chrome
```

Режимы:

```text
auto     использовать cookies только если YouTube требует подтверждение
always   всегда использовать cookies браузера
never    не использовать cookies браузера
```

Рекомендуемый режим:

```ini
cookies = auto
```

В режиме `auto` программа сначала пытается скачать видео без cookies. Если YouTube требует подтверждение:

```text
Sign in to confirm you're not a bot
```

программа получает cookies из выбранного браузера и повторяет запрос.

Примеры браузеров:

```ini
browser = chrome
```

```ini
browser = firefox
```

```ini
browser = safari
```

Пользователь должен быть авторизован на YouTube в выбранном браузере.

Cookies используются только во время работы программы и не должны сохраняться в Git.

## Куда сохраняются файлы

Программа автоматически создает каталог:

```text
video/
```

Для каждого видео создается отдельная папка:

```text
video/
└── Название видео/
    ├── Название видео.mp4
    ├── Название видео.ru.srt
    └── Название видео.en.srt
```

Каталог `video/` рекомендуется добавить в `.gitignore`.

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

## Статья на Дзен

https://dzen.ru/a/Zx-Bc5-ojxdJUm9X
