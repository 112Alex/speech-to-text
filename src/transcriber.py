import stable_whisper
from typing import List, Dict, Any

def transcribe_audio(wav_path: str) -> List[Dict[str, Any]]:
    """
    Распознает речь в WAV-файле и возвращает слова с временными метками.

    Использует модель 'medium' от OpenAI Whisper через библиотеку stable-ts
    для получения точных временных меток на уровне слов.

    Args:
        wav_path (str): Путь к WAV-файлу для транскрибации.

    Returns:
        List[Dict[str, Any]]: Список словарей, где каждый словарь
        представляет слово и содержит ключи 'word', 'start', 'end'.
        Возвращает пустой список в случае ошибки.
    """
    try:
        print("Загрузка модели распознавания речи... (может занять время при первом запуске)")
        model = stable_whisper.load_model('medium')
        
        print(f"Начало транскрибации файла: {wav_path}")
        result = model.transcribe(wav_path)
        
        # Получаем сегменты слов из результата
        word_segments = result.to_dict()['segments']
        
        all_words = []
        for segment in word_segments:
            for word_info in segment['words']:
                # stable-ts может добавлять пробелы к словам, убираем их
                word = word_info['word'].strip()
                if word: # Убедимся, что слово не пустое после очистки
                    all_words.append({
                        'word': word,
                        'start': word_info['start'],
                        'end': word_info['end']
                    })

        print("Транскрибация успешно завершена.")
        return all_words

    except Exception as e:
        print(f"Произошла ошибка во время транскрибации: {e}")
        return []
