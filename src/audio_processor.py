import os
from pydub import AudioSegment
from typing import Optional

def convert_mp3_to_wav(mp3_path: str) -> Optional[str]:
    """
    Конвертирует аудиофайл из формата MP3 в WAV.

    Функция создает WAV-файл в той же директории, что и исходный MP3,
    с тем же именем, но с расширением .wav.

    Args:
        mp3_path (str): Путь к исходному MP3 файлу.

    Returns:
        Optional[str]: Путь к созданному WAV файлу в случае успеха, иначе None.
    """
    if not os.path.exists(mp3_path):
        print(f"Ошибка: Файл не найден по пути {mp3_path}")
        return None

    wav_path = os.path.splitext(mp3_path)[0] + ".wav"
    
    try:
        print(f"Начало конвертации {mp3_path} в WAV...")
        audio = AudioSegment.from_file(mp3_path)
        audio.export(wav_path, format="wav")
        print(f"Файл успешно сконвертирован и сохранен как {wav_path}")
        return wav_path
    except Exception as e:
        print(f"Произошла ошибка при конвертации файла: {e}")
        return None
