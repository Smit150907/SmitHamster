import pymongo
import schedule
import asyncio, time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread

mongo = pymongo.MongoClient("mongodb+srv://ZeroTreasure:Smit0987@zero.9c4li.mongodb.net/?retryWrites=true&w=majority&appName=Zero")
db = mongo["BDBOT"]
users = db["users"]

api_id = '29906518'
api_hash = '76a9e84e87200fb7311a2d779a42d13a'
bot_token = '7252265143:AAGjnqnje7swU4c71tOc3AjHFA-u2e5p7R4'

app = Client("bdot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    user_id = message.from_user.id
    if not users.find_one({"user_id": user_id}):
        users.insert_one({"user_id": user_id})

async def send_messages():
    users_list = users.find()
    for user in users_list:
        try:
            inline_keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("JOIN NOW ✅", url="https://t.me/Zero_Treasure")]]
            )
            await app.send_photo(
                user["user_id"],
                photo="https://envs.sh/PxR.jpg",
                caption=(
                    '''<b>⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️
DON'T MISS 👇

Join our Main Group and get the opportunity to follow live Trading with me by following my SIGNALS for totally FREE OF COST

🔥🔥 JOIN NOW 🔥🔥

👇👇👇👇👇👇👇👇👇

https://t.me/Zero_Treasure</b>'''
                ),
                reply_markup=inline_keyboard
            )
        except Exception as e:
            print(f"Failed to send message to {user['user_id']}: {e}")

def run_scheduler():
    schedule.every(4).hours.do(lambda: asyncio.run(send_messages()))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=run_scheduler).start()
    print("bot is running")
    app.run()
