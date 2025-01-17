from src.channel import Channel
import json


class Video:
    """Класс для видео по его id"""

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео
        и методом get_response"""
        # id видео
        self.id = video_id
        try:
            # название видео
            self.title = self.get_response()['items'][0]['snippet']['title']
            # ссылка на видео
            self.url = f'https://www.youtube.com/watch?v={self.id}'
            # количество просмотров
            self.video_count = int(self.get_response()['items']
                                   [0]['statistics']['viewCount'])
            # количество лайков
            self.like_count = int(self.get_response()['items']
                                  [0]['statistics']['likeCount'])
        except TypeError:
            self.title = self.url = self.video_count = self.like_count = None

    def get_response(self):
        """
        Метод, возвращающий общую информацию о видео по его id
        """
        # Объект для работы с API youtube берём из класса Channel
        youtube = Channel.get_service()
        response = youtube.videos().list(part='snippet,statistics, '
                                              'contentDetails,topicDetails',
                                         id=self.id).execute()
        if not response['items']:
            return None
        return response

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео"""
        print(json.dumps(self.get_response(), indent=2, ensure_ascii=False))

    def __str__(self):
        """Строковое представление видео"""
        return self.title


class PLVideo(Video):
    """Класс для видео по его id и id его плейлиста"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        # id плейлиста
        self.playlist_id = playlist_id
