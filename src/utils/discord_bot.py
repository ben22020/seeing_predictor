import discord
from dotenv import load_dotenv
from src.data.get_hourly_weather import get_hourly_weather
from src.data.save_row import save_row
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID:
        return

    if message.author == client.user:
        return

    if message.content in ["1", "2", "3", "4", "5"]:
        seeing = int(message.content)
        df = get_hourly_weather(41.1034, 72.3593)
        df["seeing_quality"] = seeing
        save_row(df)
        await message.channel.send("Logged.")

client.run(TOKEN)
