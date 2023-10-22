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

# df = pd.read_csv("data.csv")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Check if the message author is the user you want to respond to
    if message.author.id == 177185585012670464 and np.random.rand() < 0.1:
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

@bot.command()
async def setup_csv(ctx):
    # Get the list of all members in the server
    members = ctx.guild.members
    user_ids = [str(member.id) for member in members]

    data = {'user_id': user_ids, 
            'balance': np.repeat(1000, len(user_ids))
    }

    df = pd.DataFrame(data)
    df.to_csv('member_balances.csv', index=False)

    # Send the list of users in a message
    await ctx.send(f"Users in this server:\n{user_ids}")

#Read csv to create a dataframe of UserData struct which contains name, ID, balances
@bot.command()
async def show_bal(ctx):
    df = pd.read_csv('member_balances.csv')
    user_array = []

    # Iterate through the rows of the DataFrame and create UserData instances
    for index, row in df.iterrows():
        user_id = row['user_id']
        username = (ctx.guild.get_member(user_id)).display_name
        balance = row['balance']

        user_data = UserData(user_id, username, balance)
        user_array.append(user_data)

    user_data_text = ""
    for user_data in user_array:
        user_data_text += str(user_data) + "\n"

    await ctx.send(user_data_text)

# @bot.command()
# async def mute(ctx, member: discord.Member):
#     # Check if the bot has the necessary permissions
#     if ctx.author.guild_permissions.mute_members:
#         # Mute the mentioned user in voice channels
#         for channel in ctx.guild.voice_channels:
#             await member.edit(mute=True)
#         await ctx.send(f"{member.mention} has been muted in voice channels.")
#     else:
#         await ctx.send("You don't have permission to use this command.")

# @bot.command()
# async def unmute(ctx, member: discord.Member):
#     if ctx.author.guild_permissions.mute_members:
#         # Unmute the mentioned user in voice channels
#         for channel in ctx.guild.voice_channels:
#             await member.edit(mute=False)
#         await ctx.send(f"{member.mention} has been unmuted in voice channels.")
#     else:
#         await ctx.send("You don't have permission to use this command.")

@bot.command()
async def get_user_id(ctx, user: discord.User):
    user_id = user.id
    await ctx.send(f"The user's ID is {user_id}")

#use private token to run the application
with open('token.txt') as f:
    token = f.readlines()

bot.run(token)