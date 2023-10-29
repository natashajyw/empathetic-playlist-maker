import asyncio
import os
import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from hume import HumeStreamClient
from hume.models.config import LanguageConfig
from dotenv import load_dotenv

from enum import Enum
from hume import HumeStreamClient
from hume.models.config import LanguageConfig

samples = [
    "Today was a fun day and I can't wait to go back to school again tomorrow."
]

attribute_list = [[0.0 for i in range(4)] for j in range(3)]

class MusAttribute(Enum):
    ENERGY = 0
    LIVENESS = 1
    LOUDNESS = 2
    TEMPO = 3

async def CallHume():
    client = HumeStreamClient("7kBEBKHVRNGmYD4OQfIusARM8g40nvEGf5cXpUiAeohJZhCE")
    config = LanguageConfig()
    async with client.connect([config]) as socket:
        for sample in samples:
            result = await socket.send_text(sample)
            emotions = result["language"]["predictions"][0]["emotions"]
            return emotions

async def DetermineAttributes():
    list = await CallHume()
    values_to_keep = ['Anger', 'Anxiety', 'Calmness', 'Distress', 'Ecstasy', 'Enthusiasm', 'Excitement', 'Joy', 'Sadness']

    emotion_list = [item for item in list if item['name'] in values_to_keep]

    emotion_list = sorted(emotion_list, key=lambda x: x['score'], reverse=True)
    emotion_list = emotion_list[:3]

    for item in emotion_list:
        print(item)

    for i in range(3):
        if emotion_list[i]['name'] == 'Anger' or emotion_list[i]['name'] == 'Distress' or emotion_list[i]['name'] == 'Anxiety' or emotion_list[i]['name'] == 'Calmness':
            attribute_list[i][MusAttribute['ENERGY'].value] = 0.3
            attribute_list[i][MusAttribute['LIVENESS'].value] = 0.3
            attribute_list[i][MusAttribute['LOUDNESS'].value] = 0.4
            attribute_list[i][MusAttribute['TEMPO'].value] = 60
        elif emotion_list[i]['name'] == 'Ecstasy' or emotion_list[i]['name'] == 'Joy' or emotion_list[i]['name'] == 'Excitement' or emotion_list[i]['name'] == 'Enthusiasm':
            attribute_list[i][MusAttribute['ENERGY'].value] = 0.8
            attribute_list[i][MusAttribute['LIVENESS'].value] = 0.8
            attribute_list[i][MusAttribute['LOUDNESS'].value] = 0.8
            attribute_list[i][MusAttribute['TEMPO'].value] = 150
        elif emotion_list[i]['name'] == 'Sadness':
            attribute_list[i][MusAttribute['ENERGY'].value] = 0.1
            attribute_list[i][MusAttribute['LIVENESS'].value] = 0.2
            attribute_list[i][MusAttribute['LOUDNESS'].value] = 0.5
            attribute_list[i][MusAttribute['TEMPO'].value] = 70

    for item in attribute_list:
        print(item)

def ReturnMusAttribute():
    return attribute_list

asyncio.run(DetermineAttributes())
song_attributes = ReturnMusAttribute()

def generate_playlist():
    scope = 'user-library-read playlist-modify-public'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)
    print("received token")
    if token:
        print("received token")
        sp = spotipy.Spotify(auth=token)
        # Get user id
        user_id = sp.current_user().get('id')
        # Create new playlist & get playlist id
        new_playlist = sp.user_playlist_create(user=user_id, name="Mood Playlist", public=True, description="")
        new_playlist_id = new_playlist.get('id')
        # Recommend Songs & Append Song URIs
        song_attributes = ReturnMusAttribute()
        print(song_attributes)
        # reccs = get_recommendations()
        reccs = sp.recommendations(seed_genres=['pop'], target_liveness=song_attributes[0][0], 
                                target_energy=song_attributes[0][1], 
                                target_loudness=song_attributes[0][2],
                                target_tempo=song_attributes[0][3], limit=20)
        print("Recommendations:")
        print(reccs)
        track_uris = [track['uri'] for track in reccs['tracks']]
        # Add tracks
        sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist_id, tracks=track_uris, position=None)
    else:
        print("Can't get token for", username)


# scope = 'user-library-read playlist-modify-public'

# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()

# token = util.prompt_for_user_token(username, scope)
# print("received token")
# if token:
#     print("received token")
#     sp = spotipy.Spotify(auth=token)
#     # Get user id
#     user_id = sp.current_user().get('id')
#     # Create new playlist & get playlist id
#     new_playlist = sp.user_playlist_create(user=user_id, name="Mood Playlist", public=True, description="")
#     new_playlist_id = new_playlist.get('id')
#     # Recommend Songs & Append Song URIs
#     song_attributes = ReturnMusAttribute()
#     print(song_attributes)
#     # reccs = get_recommendations()
#     reccs = sp.recommendations(seed_genres=['pop'], target_liveness=song_attributes[0][0], 
#                                target_energy=song_attributes[0][1], 
#                                target_loudness=song_attributes[0][2],
#                                target_tempo=song_attributes[0][3], limit=20)
#     print("Recommendations:")
#     print(reccs)
#     track_uris = [track['uri'] for track in reccs['tracks']]
#     # Add tracks
#     sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist_id, tracks=track_uris, position=None)
# else:
#     print("Can't get token for", username)
