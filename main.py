import requests
import discord
from discord import app_commands
from discord.ext import commands
import json
import time

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
atlanta_server = 1200772359376863272
atlanta = None


def get_token():
  response = requests.get("https://pastebin.com/raw/THinPpik")
  response.raise_for_status()

  return response.text  # AtlantaRP bot token

def read_config():
  with open("atlanta.json", "r") as config:
    data = json.load(config)
    return data

@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name}")
  synced = await bot.tree.sync()
  print(f"Synced {len(synced)} commands")
  global atlanta
  atlanta = discord.utils.get(bot.guilds, id=atlanta_server)

@bot.event
async def on_member_join(member):
  global atlanta
  if member.guild.id == atlanta_server:
    channel = discord.utils.get(atlanta.channels, id=1200773457806368820)
    await channel.send(f"Dobrodošel {member.mention} v AtlantaRP!")

@bot.tree.command(name="setup1", description="Setup the bot.")
@app_commands.describe(default_role = "Role given to members that join the server (ID)",
                       welcome_channel = "Channel ID of the welcome channel",
                       bot_channel = "Channel ID for the bot to send messages to")
async def setup_server(interaction: discord.Interaction,
                       default_role: str,
                       welcome_channel: str,
                       bot_channel: str):
  if interaction.user.guild_permissions.manage_guild:
    roles = []
    channels = []
    for role in atlanta.roles:
      roles.append(role)
      if str(role.id) != default_role:
        roles_list = "\n".join(roles)
        await interaction.response.send_message(f"The role you've chosen doesn't seem to exist. Here is a list of available roles and their IDs: {roles_list}")
      else:
        pass
    for channel in atlanta.channels:
      channels.append(channel)
      if str(channel.id) != welcome_channel:
        channels_list = "\n".join(channels)
        await interaction.response.send_message(f"The welcome channel you've chosen doesn't seem to exist. Here is a list of available roles and their IDs: {channels_list}")
      elif str(channel.id) != bot_channel:
        channels_list = "\n".join(channels)
        await interaction.response.send_message(f"The bot channel you've chosen doesn't seem to exist. Here is a list of available roles and their IDs: {channels_list}")
      else:
        pass
      
    await interaction.response.send_message(content=f"You've chosen these options:"
                                                          f"\nDefault role: {default_role}"
                                                          f"\nWelcome channel: {welcome_channel}"
                                                          f"\nBot channel: {bot_channel}")

    data = read_config()
    data["default_role"] = default_role
    data["welcome_channel"] = welcome_channel
    data["bot_channel"] = bot_channel

    time.sleep(3)
    await interaction.edit_original_response(content="Updated server configuration successfully.")
  else:
    await interaction.response.send_message(content="You must have **Manage server** permission in order to use this command")

bot.run(get_token())
