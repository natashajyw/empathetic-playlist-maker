import asyncio

from hume import HumeStreamClient
from hume.models.config import LanguageConfig

samples = [
    "This is unbelieveable! I really want to have pizza right now."
]

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
    print(list)

asyncio.run(function())