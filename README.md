# Конвертер Голосовых Сообщений в Текст

Программа представляет собой консольное приложение для транскрибации аудиофайлов (MP3) в текст. Она извлекает слова и их точные временные метки, сохраняет результаты в базу данных SQLite и генерирует несколько отчетов в удобных для чтения форматах.

## Технологии

- **Язык:** Python 3.9-3.11
- **Распознавание речи:** `stable-ts` (на базе OpenAI Whisper)
- **Обработка аудио:** `pydub`
- **База данных:** SQLite
- **Утилиты:** `FFmpeg`

## Установка

### 1. Системные зависимости

Перед установкой убедитесь, что у вас установлены:

- **Python 3.9-3.11:** Скачайте с [python.org](https://www.python.org/downloads/windows/). **Важно:** при установке поставьте галочку `Add Python to PATH`.
- **FFmpeg:** Скачайте сборку с [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (например, `ffmpeg-release-full.7z`), распакуйте в `C:\ffmpeg` и добавьте `C:\ffmpeg\bin` в системную переменную `PATH`.

### 2. Python-библиотеки

1.  **Создайте и активируйте виртуальное окружение:**
    ```powershell
    # Создать окружение
    python -m venv .venv

    # Активировать
    .\.venv\Scripts\Activate.ps1
    ```

2.  **Установите PyTorch:**
    - **С видеокартой NVIDIA (рекомендуется для скорости):**
      Перейдите на [сайт PyTorch](https://pytorch.org/get-started/locally/) и выберите команду установки для вашей конфигурации (CUDA).
      Пример для CUDA 12.1:
      ```powershell
      pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
      ```
    - **Без видеокарты NVIDIA (на CPU):**
      ```powershell
      pip install torch torchvision torchaudio
      ```

3.  **Установите остальные зависимости:**
    ```powershell
    pip install -r requirements.txt
    ```
    При первом запуске скрипта будет автоматически скачана модель `medium` (~1.5 ГБ).

## Использование

1.  Поместите ваш аудиофайл (например, `my_audio.mp3`) в директорию `data/input/`.

2.  Запустите главный скрипт из корневой папки проекта, указав путь к вашему файлу:
    ```powershell
    python src/main.py data/input/my_audio.mp3
    ```

3.  Результаты появятся в папке `data/output/`:
    - `my_audio.db`: База данных SQLite с результатами (`word`, `start_time`, `end_time`).
    - `my_audio.txt`: Простой текстовый отчет.
    - `my_audio.srt`: Файл субтитров для плеера.
    - `my_audio.json`: Полные данные в формате JSON.
