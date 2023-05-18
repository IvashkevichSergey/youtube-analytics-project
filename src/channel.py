import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.channel = Channel.get_service().channels().\
            list(id=channel_id, part='snippet,statistics').execute()
        # id канала
        self.id = channel_id
        # название канала
        self.title = self.channel['items'][0]['snippet']['title']
        # описание канала
        self.description = self.channel['items'][0]['snippet']['description']
        # ссылка на канал
        self.url = f'https://www.youtube.com/channel/{self.id}'
        # количество подписчиков
        self.subscribers = self.channel['items'][0]['statistics']['subscriberCount']
        # количество видео
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        # общее количество просмотров
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Классовый метод, возвращающий объект для работы с YouTube API
        """
        # Сохраняем API ключ из переменной окружения
        api_key: str = os.getenv('API_KEY')
        # Создаём объект для работы с API youtube
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def channel_id(self):
        """
        Геттер для атрибута channel_id
        """
        return self.channel_id

    def to_json(self, file_name):
        """
        Метод сохраняет в файл значения атрибутов экземпляра класса 'Channel'
        """
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.__dict__, file, indent=2, ensure_ascii=False)
