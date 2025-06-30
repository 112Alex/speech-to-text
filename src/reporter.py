import json
import os
from typing import List, Dict, Any

def _format_srt_time(seconds: float) -> str:
    """Форматирует время в секундах в формат SRT (ЧЧ:ММ:СС,МС)."""
    millisec = int((seconds - int(seconds)) * 1000)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"

class Reporter:
    """
    Класс для генерации отчетов по результатам транскрибации.
    """
    def __init__(self, words_data: List[Dict[str, Any]], output_basename: str):
        """
        Инициализирует генератор отчетов.

        Args:
            words_data (List[Dict[str, Any]]): Список данных о словах.
            output_basename (str): Базовое имя для выходных файлов (без расширения).
        """
        self.words_data = words_data
        self.output_basename = output_basename
        
        # Создаем директорию для вывода, если ее нет
        output_dir = os.path.dirname(output_basename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_all_reports(self):
        """Генерирует все доступные форматы отчетов."""
        self.generate_txt_report()
        self.generate_srt_report()
        self.generate_json_report()
        print(f"Все отчеты сохранены с базовым именем: {self.output_basename}")

    def generate_txt_report(self):
        """Генерирует отчет в формате .txt."""
        filepath = self.output_basename + ".txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            for item in self.words_data:
                start_time = item['start']
                word = item['word']
                f.write(f"[{start_time:.2f}] {word}\n")

    def generate_srt_report(self):
        """Генерирует отчет в формате субтитров .srt."""
        filepath = self.output_basename + ".srt"
        with open(filepath, 'w', encoding='utf-8') as f:
            for i, item in enumerate(self.words_data, 1):
                start_time = _format_srt_time(item['start'])
                end_time = _format_srt_time(item['end'])
                word = item['word']
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{word}\n\n")

    def generate_json_report(self):
        """Генерирует отчет в формате .json."""
        filepath = self.output_basename + ".json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.words_data, f, indent=4, ensure_ascii=False)
