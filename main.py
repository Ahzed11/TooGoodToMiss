from tgtg import TgtgClient
import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)
import time
import datetime
import os

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
USER_ID = os.environ["USER_ID"]
COOKIE = os.environ["COOKIE"]
LATITUDE = os.environ["LATITUDE"]
LONGITUDE = os.environ["LONGITUDE"]

MATRIX_USERNAME = os.environ["MATRIX_USERNAME"]
MATRIX_PASSWORD = os.environ["MATRIX_PASSWORD"]
MATRIX_URL = os.environ["MATRIX_URL"]
MATRIX_ROOM_ID = os.environ["MATRIX_ROOM_ID"]


def build_message(stores):
    msg = ""
    for store in stores:
        msg += store[0] + " - " + str(store[1])

    return msg


async def main():
    client = TgtgClient(access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN, user_id=USER_ID, cookie=COOKIE)
    async_client = AsyncClient(
        MATRIX_URL, MATRIX_USERNAME
    )
    await async_client.login(MATRIX_PASSWORD)
    print("start")

    previous_items = []
    while True:
        stores_with_items = []

        items = client.get_items(
            favorites_only=False,
            latitude=LATITUDE,
            longitude=LONGITUDE,
            radius=3,
        )

        for item in items:
            if item["items_available"] > 0:
                stores_with_items.append((item["store"]["store_name"], item["items_available"]))

        print(f"{datetime.datetime.now()} - {str(stores_with_items)}")

        if stores_with_items != previous_items:
            if len(stores_with_items) > 0:
                content = {
                    "body":  build_message(stores_with_items),
                    "msgtype": "m.text"
                }
                await async_client.room_send(MATRIX_ROOM_ID, 'm.room.message', content)
            else:
                content = {
                    "body": "Everything's gone",
                    "msgtype": "m.text"
                }
                await async_client.room_send(MATRIX_ROOM_ID, 'm.room.message', content)

        previous_items = stores_with_items
        time.sleep(10)

    await async_client.close()


asyncio.run(main())
