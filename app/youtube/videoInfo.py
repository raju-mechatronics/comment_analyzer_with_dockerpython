import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser
import datetime


def get_rate_per_day(date_string, count):
    uploadDate = parser.parse(date_string)
    today = datetime.datetime.now(datetime.timezone.utc)
    totalDays = (today - uploadDate).days
    return round(count / totalDays)


def get_video_info(video_id):
    youtube = build("youtube", "v3", developerKey=os.getenv("youtube_api_key"))

    try:
        video_response = (
            youtube.videos().list(part="statistics,snippet", id=video_id).execute()
        )

        video_info = video_response["items"][0]

        upload_date = video_info["snippet"]["publishedAt"]
        total_views = int(video_info["statistics"]["viewCount"])
        num_comments = int(video_info["statistics"]["commentCount"])
        num_likes = int(video_info["statistics"]["likeCount"])

        view_rate_per_day = get_rate_per_day(upload_date, total_views)
        comment_rate_per_day = get_rate_per_day(upload_date, num_comments)
        like_rate_per_day = get_rate_per_day(upload_date, num_likes)

        return {
            "upload_date": upload_date,
            "view_count": total_views,
            "comment_count": num_comments,
            "like_count": num_likes,
            "view_rate": view_rate_per_day,
            "comment_rate": comment_rate_per_day,
            "like_rate": like_rate_per_day,
        }

    except HttpError as e:
        print("An error occurred: %s" % e)
        return None
