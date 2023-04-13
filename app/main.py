from dotenv import load_dotenv
load_dotenv()
#import envs before everything else



from database.engine import engine
from database import models


from fastapi import FastAPI
from comment.youtube import YoutubeComment
from huggignface import count_comment_type
import uvicorn

models.Base.metadata.create_all(engine)



app = FastAPI()

@app.get("/")
async def root(videoId:str):
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