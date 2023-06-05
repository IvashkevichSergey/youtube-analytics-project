import re
import datetime
from src.video import Video
from src.channel import Channel


class PlayList:
    """Класс для видео по id его плейлиста"""

    # Объект для работы с API youtube берём из класса Channel
    youtube = Channel.get_service()

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_channel_name()
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def get_response(self):
        """
        Метод, возвращающий общую информацию о плейлисте по его id
        """
        playlist_videos = self.youtube.playlistItems().list(playlistId=
                                                            self.playlist_id,
                                                            part='snippet',
                                                            maxResults=50,
                                                            ).execute()

        return playlist_videos

    def get_channel_name(self):
        """
        Метод, возвращающий название плейлиста
        """
        playlist_info = self.youtube.playlists().list(part='snippet',
                                                      id=self.playlist_id,
                                                      fields='items(snippet'
                                                             '(title))'
                                                      ).execute()
        channel_title = playlist_info['items'][0]['snippet']['title']
        return channel_title

    @property
    def total_duration(self):
        """
        Метод, возвращающий объект класса datetime.timedelta
        с суммарной длительность плейлиста
        """
        # Создаём объект класса datetime.timedelta
        duration = datetime.timedelta()
        # Проходим по всем видео плейлиста
        for video in self.get_response()['items']:
            # Через класс Video находим информацию о длительности видео
            pl_video = Video(video['snippet']['resourceId']
                             ['videoId']).get_response()
            duration_str = pl_video['items'][0]['contentDetails']['duration']

            # "Вырезаем" минуты и секунды из строки с продолжительностью видео
            x = re.findall(r'PT(\d*)M?(\d*)S?', duration_str)[0]
            minutes = int(x[0]) if x[0] else 0
            seconds = int(x[1]) if x[1] else 0

            # Суммируем время всех видео
            duration += datetime.timedelta(minutes=minutes, seconds=seconds)
        return duration

    def show_best_video(self):
        """
        Метод, возвращающий ссылку на самое популярное
        видео из плейлиста (по количеству лайков)
        """
        best_video_url = None
        best_video_likes = 0

        # Проходим по всем видео плейлиста
        for video in self.get_response()['items']:

            # Создаём объекты класса Video
            video_id = video['snippet']['resourceId']['videoId']
            pl_video = Video(video_id)

            # Используем метод view_count класса Video для
            # получения информации о количестве лайков
            if int(pl_video.like_count) > best_video_likes:
                best_video_url = f'https://youtu.be/{video_id}'

        return best_video_url
