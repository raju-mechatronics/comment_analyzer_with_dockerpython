import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import openai
from youtube_transcript_api import YouTubeTranscriptApi

# print python version
import sys

print(sys.version)

# set openai api key
openai.api_key = os.getenv("chat_gpt_api_key")


def getTranscript(videoId):
    # assigning srt variable with the list
    # of dictionaries obtained by the get_transcript() function
    srt = YouTubeTranscriptApi.get_transcript(videoId)

    return " ".join([s["text"] for s in srt])


# summerize text with chatgpt 3.5
def summarize_text(text):
    if text is not None:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            prompt=[
                {
                    "role": "user",
                    "content": f"Summarize this with good puntuation: {text}",
                },
            ],
        )
        print(response["choices"])
        summary = response["choices"][0]["message"]["content"]
        return summary
    else:
        return None


def get_video_summary(video_id):
    captions = getTranscript(video_id)
    if captions:
        summary = summarize_text(captions)
        return summary
    return None


print(get_video_summary("SW14tOda_kI"))
