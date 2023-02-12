import os
import discord
from discord.ext import commands
import responses


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)




def run_discord_bot():
    token = "MTA1MDAyOTQyODQ2MzM3ODQ5Mw.GGQQkr.DR8qlfCrhCJkADH8lUknccJAv9RY18eVkWONy8"
    BOT_FLAG = '!'

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said {user_message} in channel {channel}")
        try:
            if user_message[0] == '?':
                await send_message(message, user_message[1:],  is_private=True)
            elif user_message[0] == BOT_FLAG:
                await send_message(message, user_message[1:], is_private=False)
                print("bot falg working")
            else:
                pass
        except Exception as e:
            print(e)

    @client.event
    async def on_member_join(member):
        channel_id = 1074133871962099732
        channel = client.get_channel(channel_id)
        await channel.send(f'{member} has now officially become a loser')

    @client.event
    async def on_member_remove(member):
        channel_id = 1074133871962099732
        channel = client.get_channel(channel_id)
        await channel.send(f"{member} has regained it's connection the outer world")


    client.run(token)
