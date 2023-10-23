import discord
from discord.ext import commands
import numpy as np
import pandas as pd
from data_structures import *

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_array = []

@bot.event
async def on_ready():
    try:
        df = pd.read_csv('user_data.csv')
        for index, row in df.iterrows():
            user_id = row['User ID']
            username = row['Username']
            balance = row['Balance']
            user = UserData(user_id, username, balance)
            user_array.append(user)

        print('bot started')

    except FileNotFoundError:
        df = pd.DataFrame(columns=['User ID', 'Username', 'Balance'])
        df.to_csv('user_data.csv', index=False)
        print("user_data.csv not found. Creating a new file.")

@bot.event
async def on_shutdown():
    print("Shutting down...")
    await bot.close()

@bot.event
async def on_message(message):
    # Check if the message author is the user you want to respond to
    if message.author.id == 177185585012670464 and np.random.rand() < 0.5:
        response = "jon ur a rat"
        await message.channel.send(response)

    # Include this line to allow other event handlers to process the message
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    # Check if the bot is mentioned in the message content
    if bot.user.mentioned_in(message):
        # Respond to the mention
        await message.channel.send(f"hi")
    await bot.process_commands(message)

#Read csv to create a dataframe of UserData struct which contains name, ID, balances
@bot.command()
async def show_server_bal(ctx):
    user_data = ""
    for user in user_array:
        user_data += str(user) + "\n"

    await ctx.send(user_data)

@bot.command()
async def bet(ctx, wager: int):
    # Find the UserData object for the user who placed the bet
    user_id = ctx.author.id
    user = next((u for u in user_array if u.user_id == user_id), None)

    if user is None:
        # Create a new UserData instance if the user doesn't exist in the list
        # username = (ctx.guild.get_member(user_id)).display_name
        user = UserData(user_id, ctx.author.display_name, 1000)  # Initial balance
        user_array.append(user)

    if user.balance < wager:
        await ctx.send("You don't have enough balance to place this bet.")
        return

    # Simulate a random result (you can implement your own logic)
    import random
    result = random.choice(["win", "lose"])

    if result == "win":
        user.balance += wager
        await ctx.send(f"You won {wager}! Your new balance is {user.balance}.")
    else:
        user.balance -= wager
        await ctx.send(f"You lost {wager}! Your new balance is {user.balance}.")

@bot.command()
async def check_bal(ctx):
    user_id = ctx.author.id
    user = next((u for u in user_array if u.user_id == user_id), None)
    if user is not None:
        await ctx.send(str(user))
    else:
        await ctx.send("You don't have a balance record. Please use the `!bet` command to create one.")

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

@bot.command()
async def get_user_id(ctx, user: discord.User):
    user_id = user.id
    await ctx.send(f"The user's ID is {user_id}")

@bot.command()
async def stop(ctx):
    if await bot.is_owner(ctx.author):
        user_data = [
            {
                'User ID': user.user_id,
                'Username': user.username,
                'Balance': user.balance
            }
            for user in user_array
        ]

        df = pd.DataFrame(user_data)
        df.to_csv('user_data.csv', index=False)

        await ctx.send("Shutting down...")
        await on_shutdown()
    else:
        await ctx.send("You do not have permission to shut down the bot.")

#use private token to run the application
with open('token.txt') as f:
    token = f.read()
bot.run(token)