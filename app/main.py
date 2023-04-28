from dotenv import load_dotenv

load_dotenv()


# import envs before everything else
from youtube.caption import get_video_summary
from youtube.videoInfo import get_video_info

from database.engine import engine
from database import models

from fastapi import FastAPI
from comment.youtube import YoutubeComment
from huggignface import count_comment_type
import uvicorn

models.Base.metadata.create_all(engine)


app = FastAPI()


@app.get("/videoInfo")
async def videoInfo(videoId: str):
    if videoId is not None:
        try:
            res = get_video_info(videoId)
            return res
        except:
            return {"message": "Please provide a valid videoId"}
    else:
        return {"message": "Please provide a videoId"}


@app.get("/videoSummery")
async def videoSummery(videoId: str):
    print("summery")
    if videoId is not None:
        try:
            summery = get_video_summary(videoId)
            if summery is None:
                return {"this video has no caption"}
            return summery
        except:
            return {"message": "Please provide a valid videoId"}


@app.get("/")
async def root(videoId: str):
    if videoId is not None:
        try:
            comments = YoutubeComment(videoId)
            res = comments.get_result()
            return res
        except:
            return {"message": "Please provide a valid videoId"}
    else:
        return {"message": "Please provide a videoId"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
