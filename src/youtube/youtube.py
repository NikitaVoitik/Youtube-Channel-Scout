from googleapiclient import discovery
from utils import month_before_rfc3339
from utils import load_json

COUNTRY_INFO = load_json('../../data/countries.json')


class YouTubeService:
    def __init__(self, api_key):
        self.__yt = None
        self.api_key = api_key
        self._build_youtube_service()

    def _build_youtube_service(self) -> None:
        self.__yt = discovery.build('youtube', 'v3', developerKey=self.api_key)

    def search_channels(self, search_query: str, country: str = 'United States', max_results: int = 50) -> list:
        search_response = self.__yt.search().list(
            q=search_query,
            part='snippet',
            maxResults=max_results,
            type='video',
            publishedAfter=month_before_rfc3339(),
            regionCode=COUNTRY_INFO[country]['regionCode'],
            relevanceLanguage=COUNTRY_INFO[country]['relevanceLanguage'],
        ).execute()

        search_results = []
        for item in search_response['items']:
            video_data = {
                'channel_id': item['snippet']['channelId'],
                'channel_title': item['snippet']['channelTitle'],
            }
            if video_data not in search_results:
                search_results.append(video_data)
        return search_results

    def get_upload_playlist_id(self, channel_id: str) -> str:
        request = self.__yt.channels().list(
            part='contentDetails',
            id=channel_id
        )
        response = request.execute()
        upload_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return upload_playlist_id

    def get_videos_from_playlist(self, playlist_id: str) -> dict:
        response = self.__yt.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50
        ).execute()
        return response['items']

    def get_videos_from_upload_playlist(self, channel_id: str) -> dict:
        playlist_id = self.get_upload_playlist_id(channel_id)
        videos = self.get_videos_from_playlist(playlist_id)
        return videos

    def get_video_statistics(self, video_id: str) -> dict:
        response = self.__yt.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        ).execute()
        return response['items'][0]

    def get_videos_statistics(self, videos: list) -> list:
        video_ids = [videos[ind]['contentDetails']['videoId'] for ind in range(0, min(50, len(videos)))]
        statistics = []
        for video_id in video_ids:
            stats = self.get_video_statistics(video_id)
            statistics.append({
                'title': stats['snippet']['title'],
                'video_id': stats['id'],
                'view_count': stats['statistics'].get('viewCount', 0),
                'like_count': stats['statistics'].get('likeCount', 0),
                'comment_count': stats['statistics'].get('commentCount', 0),
                'duration': stats['contentDetails'].get('duration', 0)
            })

        return statistics

    def get_last_videos_statistics(self, videos: dict, number_of_videos: int = 8) -> list:
        videos = videos[:number_of_videos]
        sorted_videos = sorted(videos, key=lambda video: video['contentDetails']['videoPublishedAt'], reverse=True)
        statistics = self.get_videos_statistics(sorted_videos)
        return statistics

    def get_channel_info(self, channel_id: str) -> dict:
        response = self.__yt.channels().list(
            part='snippet',
            id=channel_id
        ).execute()
        channel_info = response['items'][0]['snippet']
        return channel_info