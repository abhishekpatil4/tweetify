import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_tweet_text_by_id(tweet_id):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    bearer_token = os.getenv("TWITTER_TOKEN")
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']['text'].replace('\n', '')
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_user_id_by_username(username):
    url = f"https://api.x.com/2/users/by/username/{username}"
    bearer_token = os.getenv("TWITTER_TOKEN")
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']['id']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_user_data_by_username(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    bearer_token = os.getenv("TWITTER_TOKEN")
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    params = {
        'user.fields': 'description,id,name,profile_image_url,username'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print("Username not found.")
        elif response.status_code == 429:
            print("Too many requests. Please try again later.")
        else:
            print(f"HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None