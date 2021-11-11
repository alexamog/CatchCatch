import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if 'happy birthday' in message.content.lower():
        await message.channel.send(f'Happy Birthday! {client.user}')
client.run(TOKEN)
