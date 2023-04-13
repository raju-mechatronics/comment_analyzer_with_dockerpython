import json
import os

from googleapiclient.discovery import build
from typing import List
from dataclasses import dataclass
import numpy as np

from database.models import YoutubeCommentModel, YoutubeResultModel
from database.engine import dbSession as db

from huggignface import count_comment_type


@dataclass
class Comment:
    text: str
    likeCount: int
    publishedAt: str
    channelId: str
    replies: List["Comment"]
    def parse_in_json(self):
        replies = []
        if self.replies:
            replies = [reply.parse_in_json() for reply in self.replies]
        return {
            "text": self.text,
            "likeCount": self.likeCount,
            "publishedAt": self.publishedAt,
            "channelId": self.channelId,
            "replies": replies
        }

    @staticmethod
    def parse_from_json(obj: dict) -> "Comment":
        replies = []
        if obj.get('replies'):
            replies = [Comment.parse_from_json(reply) for reply in obj.get('replies') if reply is not None]
        return Comment(text=obj['text'], publishedAt=obj['publishedAt'], likeCount=obj['likeCount'],
                       channelId=obj['channelId'],
                       replies=replies)

    def parse_in_numpy_array(self):
        return np.array([self.text, self.likeCount, self.publishedAt, self.channelId])


def make_comment_from_snippet(obj: dict) -> Comment:
    d = {"text": obj.get('snippet', {}).get('textOriginal'), "likeCount": obj.get('snippet', {}).get('likeCount'),
         "publishedAt": obj.get('snippet', {}).get('publishedAt'),
         "channelId": obj.get('snippet', {}).get('authorChannelId', {}).get('value')}
    return Comment(text=d['text'], publishedAt=d['publishedAt'], likeCount=d['likeCount'], channelId=d['channelId'],
                   replies=None)


def get_comment_from_obj(obj: dict) -> Comment:
    toplevel = obj.get('snippet').get('topLevelComment')
    replies = obj.get('replies', {}).get('comments', [])
    comment = make_comment_from_snippet(toplevel)
    comment.replies = [make_comment_from_snippet(reply) for reply in replies if reply]
    return comment


def get_comments(videoId: str, maxPull=1000) -> List[Comment]:
    youtube = build('youtube', 'v3', developerKey=os.getenv('youtube_api_key'))
    commentResponse: dict = youtube.commentThreads().list(
        part="snippet",
        videoId=videoId,
        maxResults=100,
        order="relevance"
    ).execute()
    allComment: List[Comment] = []
    for comment in commentResponse.get("items"):
        allComment.append(get_comment_from_obj(comment))
    pulled = 1
    while commentResponse.get('nextPageToken', False) and pulled < int(maxPull / 100):
        pulled += 1
        commentResponse = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=videoId,
            maxResults=100,
            order="relevance",
            pageToken=commentResponse.get('nextPageToken')
        ).execute()
        for comment in commentResponse.get("items"):
            allComment.append(get_comment_from_obj(comment))
    return allComment


class YoutubeComment:
    def __init__(self, videoId: str, maxPull=1000):
        youtubeComment = db.query(YoutubeCommentModel).filter(YoutubeCommentModel.videoId == videoId).first()
        if youtubeComment is None:
            data = get_comments(videoId, maxPull)
            youtubeComment = YoutubeCommentModel(videoId=videoId,
                                                 comments=json.dumps([comment.parse_in_json() for comment in data]))
            db.add(youtubeComment)
            db.commit()
        self.videoId = videoId
        self.comments = [Comment.parse_from_json(comment) for comment in json.loads(youtubeComment.comments)]

    def get_result(self):
        result = db.query(YoutubeResultModel).filter(YoutubeResultModel.videoId == self.videoId).first()
        if result is None:
            comments = ([comment.text for comment in self.comments])
            res = count_comment_type(comments)
            result = YoutubeResultModel(videoId=self.videoId, result=json.dumps(res))
            db.add(result)
            db.commit()
        return json.loads(result.result)

