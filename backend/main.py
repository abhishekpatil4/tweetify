from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from firebase.init import auth
from composio_config import createNewEntity, isEntityConnected, createTwitterIntegrationAndInitiateAdminConnection
import logging
from quote_generator import generate_repost_quote
from new_tweet_repost import create_new_tweet_and_repost
from twitter_functions import get_tweet_text_by_id, get_user_data_by_username
from repost_existing_tweet import repost_existing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "https://tweetify-three.vercel.app",
    "http://localhost:5173",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_token(auth_credentials: HTTPAuthorizationCredentials = Depends(
    HTTPBearer())):
    token = auth_credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Pydantic models
class UserData(BaseModel):
    admin_username: str
    username: str
    appType: str

class TwitterUserData(BaseModel):
    username: str

class InitialiseAgentData(BaseModel):
    username: str

class TweetData(BaseModel):
    prompt: str
    tweetContent: str
    numberOfQuotes: int

class GetTweetData(BaseModel):
    tweet_id: str

class TweetRequestData(BaseModel):
    initial_tweet_entity_id: str
    post: str
    repost_data_list: list

class RepostExistingData(BaseModel):
    admin_entity_id: str
    tweet_id: str
    repost_data_list: list

class NewIntegrationData(BaseModel):
    username: str
    redirectUrl: str

class NewEntityData(BaseModel):
    username: str
    newUserId: str
    redirectUrl: str

@app.post("/newintegration")
async def handle_request(user_data: NewIntegrationData,
                         decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token['uid']
    username = user_data.username
    redirectUrl = user_data.redirectUrl
    res = createTwitterIntegrationAndInitiateAdminConnection(username, redirectUrl)
    return res

@app.post("/newentity")
async def handle_request(user_data: NewEntityData,
                         decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token['uid']
    username = user_data.username
    newUserId = user_data.newUserId
    redirectUrl = user_data.redirectUrl
    res = createNewEntity(username, newUserId, redirectUrl)
    return res

@app.post("/checkconnection")
async def handle_request(user_data: UserData,
                         decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token['uid']
    admin_username = user_data.admin_username
    username = user_data.username
    appType = user_data.appType
    res = isEntityConnected(admin_username, username, appType)
    return res

@app.post("/getquotes")
async def handle_request(tweet_data: TweetData,
                         decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token['uid']
    prompt = tweet_data.prompt
    tweet_content = tweet_data.tweetContent
    number_of_quotes = tweet_data.numberOfQuotes
    res = generate_repost_quote(prompt, tweet_content, number_of_quotes)
    return {"quotes": res}

@app.post("/newtweetandrepost")
async def handle_request(tweet_request_data: TweetRequestData,
                         decoded_token: dict = Depends(verify_token)):
    initial_tweet_entity_id = tweet_request_data.initial_tweet_entity_id
    initial_tweet = tweet_request_data.post
    repost_data_list = tweet_request_data.repost_data_list
    res = create_new_tweet_and_repost(initial_tweet_entity_id, initial_tweet, repost_data_list)
    return {"result": res}


@app.post("/repostexisting")
async def handle_request(tweet_request_data: RepostExistingData,
                         decoded_token: dict = Depends(verify_token)):
    admin_entity_id = tweet_request_data.admin_entity_id
    tweet_id = tweet_request_data.tweet_id
    repost_data_list = tweet_request_data.repost_data_list
    res = repost_existing(admin_entity_id, tweet_id, repost_data_list)
    return {"result": res}

@app.post("/gettweet")
async def handle_request(tweet_data: GetTweetData, decoded_token: dict = Depends(verify_token)):
    tweet_id = tweet_data.tweet_id
    try:
        tweet_text = get_tweet_text_by_id(tweet_id)
        return {"tweet_text": tweet_text}
    except requests.exceptions.RequestException as e:
        if e.response.status_code == 400:
            return {"error": "An error occurred: 400 Client Error: Bad Request for url: https://api.twitter.com/2/tweets"}, 400
        return {"error": str(e)}, 500

@app.post("/getusertwitterdata")
async def handle_request(user_data: TwitterUserData, decoded_token: dict = Depends(verify_token)):
    username = user_data.username
    try:
        res = get_user_data_by_username(username)
        if res is None:
            return {"error": "An error occurred while fetching user data."}, 500
        return res
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": "Username not found."}, 404
        elif e.response.status_code == 429:
            return {"error": "Too many requests. Please try again later."}, 429
        else:
            return {"error": f"HTTP error occurred: {e}"}, e.response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}, 500

@app.get("/")
async def handle_request():
    return "ok"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start the server (if running locally)
# Run the following command in your terminal: uvicorn main:app --reload
