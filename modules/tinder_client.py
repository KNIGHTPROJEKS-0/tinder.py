import asyncio
import os
from dotenv import load_dotenv
import tinder

load_dotenv()


class Client(tinder.Client):
    teaser_ids = set()

    async def get_teasers(self):
        while True:
            teasers = await self.fetch_teasers()
            self.teaser_ids |= {teaser.id for teaser in teasers}
            await asyncio.sleep(60)

    async def get_recs(self):
        while True:
            users = await self.fetch_recs()
            print(f"Fetched {len(users)} users")
            for user in users:
                photo_ids = {photo.id for photo in user.photos}
                if not self.teaser_ids.isdisjoint(photo_ids):
                    await user.like()
            await asyncio.sleep(60)

    async def run_bot(self):
        await asyncio.gather(self.get_teasers(), self.get_recs())


def start_client():
    token = os.getenv("TINDER_AUTH_TOKEN")
    if not token:
        raise ValueError("TINDER_AUTH_TOKEN not found in .env")

    client = Client()
    client.run(token)
