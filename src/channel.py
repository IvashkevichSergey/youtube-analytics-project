import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    # Сохраняем API ключ из переменной окружения
    api_key: str = os.getenv('API_KEY')
    # Создаём объект для работы с API youtube
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
