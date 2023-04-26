import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_video_info(video_id):
    youtube = build('youtube', 'v3', developerKey=os.getenv('youtube_api_key'))

    try:
        video_response = youtube.videos().list(
            part='statistics,snippet',
            id=video_id
        ).execute()

        video_info = video_response['items'][0]

        upload_date = video_info['snippet']['publishedAt']
        total_views = int(video_info['statistics']['viewCount'])
        num_comments = int(video_info['statistics']['commentCount'])
        num_likes = int(video_info['statistics']['likeCount'])

        return {"upload_date": upload_date, "view_count": total_views, "comment_count": num_comments, "like_count": num_likes}

    except HttpError as e:
        print("An error occurred: %s" % e)
        return None


