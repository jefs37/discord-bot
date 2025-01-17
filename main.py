import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from data_structures import *
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
        print('bot started')

@bot.event
async def on_shutdown():
    print("Shutting down...")
    await bot.close()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # message Jon specifically
    if message.author.id == 177185585012670464 and np.random.rand() < 1:
        response = "jon ur a rat"
        await message.channel.send(response)

    if 'a' in message.content.lower():
        message_J = message.content.replace('A', 'J').replace('a', 'j')
        await message.channel.send('Did you mean to type: ' + message_J)

    # Include this line to allow other event handlers to process the message
    await bot.process_commands(message)

# mute and unmute
@bot.command()
async def mute(ctx, member: discord.Member):
    # Check if the bot has the necessary permissions
    if ctx.author.guild_permissions.mute_members:
        # Mute the mentioned user in voice channels
        for channel in ctx.guild.voice_channels:
            await member.edit(mute=True)
        await ctx.send(f"{member.mention} has been muted in voice channels.")
    else:
        await ctx.send("You don't have permission to use this command.")

@bot.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.mute_members:
        # Unmute the mentioned user in voice channels
        for channel in ctx.guild.voice_channels:
            await member.edit(mute=False)
        await ctx.send(f"{member.mention} has been unmuted in voice channels.")
    else:
        await ctx.send("You don't have permission to use this command.")

# get user ID
@bot.command()
async def get_user_id(ctx, user: discord.User):
    user_id = user.id
    await ctx.send(f"The user's ID is {user_id}")

#use private token to run the application
with open('token.txt') as f:
    token = f.read()
bot.run(token)