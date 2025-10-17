import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = 'MrBeast'
maxResult = 50



def get_playlist_id():
    try:
        url =   f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'
        responce  = requests.get(url)
        responce.raise_for_status()
        data = responce.json()

        # print(json.dumps(data, indent=4))
        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        # print(channel_playlistId)
        return channel_playlistId


    except requests.exceptions.RequestException as e:
        raise e

def get_video_ids(playlistId):
        
        video_ids = []

        pageToken = None

        base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResult}&playlistId={playlistId}&key={API_KEY}'

        try:
            while True:
                url = base_url

                if pageToken:
                     url += f'&pageToken={pageToken}'
                
                responce  = requests.get(url)
                responce.raise_for_status()
                data = responce.json()

                for item in data.get('items', []):
                     video_id = item['contentDetails']['videoId']

                     video_ids.append(video_id)
                     
                
                pageToken = data.get('nextPageToken')

                if not pageToken:
                     break
            return video_ids
                
        except requests.exceptions.RequestException as e:
             raise e
        


if __name__ == '__main__':
    playlistId = get_playlist_id()
    get_video_ids(playlistId)