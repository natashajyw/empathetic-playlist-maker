import asyncio

from enum import Enum
from hume import HumeStreamClient
from hume.models.config import LanguageConfig

samples = [
    "Today is a great day. I absolutely love the weather we have and I can't wait to get started with work today."
]

class MusAttribute(Enum):
    ENERGY = 0
    LIVENESS = 1
    LOUDNESS = 2
    TEMPO = 3

async def main():
    client = HumeStreamClient("7kBEBKHVRNGmYD4OQfIusARM8g40nvEGf5cXpUiAeohJZhCE")
    config = LanguageConfig()
    async with client.connect([config]) as socket:
        for sample in samples:
            result = await socket.send_text(sample)
            emotions = result["language"]["predictions"][0]["emotions"]
            return emotions

async def function():
    list = await main()
    values_to_keep = ['Anger', 'Anxiety', 'Calmness', 'Distress', 'Ecstasy', 'Enthusiasm', 'Excitement', 'Joy', 'Sadness']

    emotion_list = [item for item in list if item['name'] in values_to_keep]

    emotion_list = sorted(emotion_list, key=lambda x: x['score'], reverse=True)
    emotion_list = emotion_list[:3]

    for item in emotion_list:
        print(item)

    attribute_list = [[0.0 for i in range(4)] for j in range(3)]

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

asyncio.run(function())




