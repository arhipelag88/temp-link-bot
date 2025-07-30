from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import random
import time

API_ID = 12345678  # <-- встав свій API ID
API_HASH = "your_api_hash"  # <-- встав свій API HASH
BOT_TOKEN = "your_bot_token"  # <-- встав токен від BotFather

app = Client("temp_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

channels = {
    "MAIN": "-1001234567890",
    "VOUCHES": "-1009876543210",
    "CHAT": "-1001111222233",
    "PREPAIDS": "-1004444555566"
}

def generate_math():
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    return a, b, a + b

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    a, b, result = generate_math()
    await message.reply_text(f"🔒 Solve to get invites:\n\n{a} + {b} = ?")

    def check_response(_, m: Message):
        return m.from_user.id == message.from_user.id and m.text.isdigit()

    try:
        response = await app.listen(message.chat.id, timeout=30)
        if int(response.text) == result:
            await message.reply_text("✅ Correct—fetching invites...")

            text = "📩 *Your links (valid for 20s):*\n"
            now = int(time.time())

            for name, chat_id in channels.items():
                invite = await app.create_chat_invite_link(chat_id, expire_date=now + 20)
                text += f"- {name}: {invite.invite_link}\n"

            await message.reply_text(text, parse_mode="Markdown")
        else:
            await message.reply_text("❌ Wrong answer. Try /start again.")
    except asyncio.TimeoutError:
        await message.reply_text("⏱ Time's up. Try /start again.")

app.run()

