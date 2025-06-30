import argparse
import os
import sys

# Добавляем корневую директорию проекта в sys.path для корректных импортов
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from src.audio_processor import convert_mp3_to_wav
from src.transcriber import transcribe_audio
from src.database_manager import DatabaseManager
from src.reporter import Reporter

def main():
    """
    Главная функция, управляющая процессом транскрибации аудиофайла.
    """
    parser = argparse.ArgumentParser(description="Транскрибатор аудиофайлов с сохранением в БД и генерацией отчетов.")
    parser.add_argument("input_file", type=str, help="Путь к входному MP3 файлу.")
    args = parser.parse_args()

    input_mp3_path = args.input_file

    if not os.path.exists(input_mp3_path):
        print(f"Ошибка: Входной файл не найден по пути: {input_mp3_path}")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(input_mp3_path))[0]
    output_dir = os.path.join(project_root, 'data', 'output')
    output_basename = os.path.join(output_dir, base_name)
    db_path = output_basename + ".db"

    # Проверка и подготовка путей
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Конвертация MP3 в WAV
    wav_path = convert_mp3_to_wav(input_mp3_path)
    if not wav_path:
        print("Не удалось сконвертировать MP3 в WAV. Завершение работы.")
        sys.exit(1)

    try:
        # Транскрибация аудио
        words_data = transcribe_audio(wav_path)
        if not words_data:
            print("Транскрибация не дала результатов. Проверьте аудиофайл.")
            sys.exit(1)

        # Сохранение в базу данных
        db_manager = DatabaseManager(db_path)
        db_manager.save_words(words_data)

        # Генерация отчетов
        reporter = Reporter(words_data, output_basename)
        reporter.generate_all_reports()

        print("\nРабота успешно завершена!")

    finally:
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)
            print(f"\nВременный файл {wav_path} удален.")

if __name__ == "__main__":
    main()
