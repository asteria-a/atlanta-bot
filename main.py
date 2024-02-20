import discord
from discord import app_commands, File
from discord.ext import commands, tasks
import datetime
import base64
from easy_pil import Editor, load_image_async, Font
import os
import io
import asyncio
import threading

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
atlanta_server = 1200772359376863272
default_role = 1200844380328702113
welcome_channel =1200773457806368820
bot_logs = 1200845729086841012

def get_token():
  token = base64.b64decode("TVRJd01EZ3pNREV6TURBeE16QTNOelV4TlEuR1diclhDLnVYWXYxanJMTjlFY0xRaUV5dDBoXzZ2cThSS1ZsRWRBODZfaldN")
  return token.decode("utf-8")

def currenttime():
    formatted = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime("%H:%M:%S (%d.%m.%Y)")
    return formatted

async def gen_img(member):
    try:
        cwd = os.getcwd()
        bg_path = os.path.join(cwd, "assets", "background.png")

        bg = Editor(bg_path)
        avatar = await load_image_async(str(member.display_avatar.url))
        # Increase the size of the profile image slightly
        profile_width, profile_height = (180, 180)

        profile = Editor(avatar).resize((profile_width, profile_height)).circle_image()
        bg_width, bg_height = (600, 400)

        # Calculate coordinates to center the profile image
        x_centered = (bg_width - profile_width) // 2
        y_centered = (bg_height - profile_height) // 2

        font_path = os.path.join(cwd, "assets", "font.ttf")

        bg.paste(profile, (x_centered, (y_centered - 45)))

        bg.text((300, 260), "Dobrodošel", color="white", font=Font(font_path, size=45), align="center", stroke_fill="black", stroke_width=5)
        bg.text((300, 310), f"{member.display_name}", color="white", font=Font(font_path, size=45), align="center", stroke_fill="black", stroke_width=5)
        bg.text((300, 350), "v AtlantaRP", color="white", font=Font(font_path, size=45), align="center", stroke_fill="black", stroke_width=5)

        # Save the image bytes to a BytesIO buffer
        image_buffer = io.BytesIO()
        bg.image.save(image_buffer, format="PNG")

        # Set the buffer's position to the beginning for reading
        image_buffer.seek(0)

        # Return the BytesIO buffer directly
        return File(image_buffer, f"{member.display_name}.png")

    except Exception as e:
        print(f"Error generating image: {e}")
        raise  # Re-raise the exception for the caller to handle
    
@tasks.loop(seconds=180)
async def update_server_stats():
  try:
    server = discord.utils.get(bot.guilds, id=atlanta_server)
    tracker = discord.utils.get(server.channels, id=1202260969963659304)
    await tracker.edit(name=f"Vseh memberjev: {len(atlanta.members)}")
    return "Successfully updated server stats"
  except discord.HTTPException as e:
     print(f"An error occured while updating the server stats: {e}")
     return e

@bot.event
async def on_ready():
    print(f"{bot.user.display_name} ({bot.user.id}) bot logged in at {currenttime()}")
    
    synced = await bot.tree.sync()
    global atlanta
    atlanta = discord.utils.get(bot.guilds, id=atlanta_server)
    log = discord.utils.get(atlanta.channels, id=bot_logs)
    await log.send(content=f"**Bot logged in at {currenttime()}**\nBot info:\nUsername: {bot.user.name}\nID: {bot.user.id}\nSynced commands: {len(synced)} command(s)")
    await update_server_stats()

@bot.event
async def on_member_join(member):
    if member.guild.id == atlanta_server:
        channel = discord.utils.get(atlanta.channels, id=welcome_channel)
        role = discord.utils.get(atlanta.roles, id=default_role)
        await member.add_roles(role)
        member_id = member.id
        try:
            await channel.send(f"Dobrodošel <@{member_id}> v AtlantaRP", file=await gen_img(member))
        except Exception as e:
            print(f"Error generating and sending image: {e}")

@bot.event
async def on_raw_member_remove(payload):
  channel = discord.utils.get(atlanta.channels, id=welcome_channel)
  member_id = payload.user.id

  await channel.send(content=f"<@{member_id}> nas je zapustil.")

"""async def cmd_exc(action=None, *args, **kwargs):
    try:
        if action == "rearrange":
            if len(args) == 0:
                # If the user just types "rearrange", return the syntax for the command
                print("Syntax:\n'rearrange pos' - Returns a list of roles and their position integer.\n'rearrange <role-id> <pos>' - Moves role to set pos")
            elif len(args) == 1:
                if args == "pos":
                    roles = atlanta.roles
                    sorted_roles = sorted(roles, key=lambda x: x.position, reverse=True)
                    pos_list = {role.name: role.position for role in sorted_roles}
                    print("Current role positions:")
                    print(pos_list)
                    
            elif len(args) == 2:
                # If the user types "rearrange <role_id> <position>", move the role to the specified position
                role_id, new_position = args
                role_id = args[0]
                new_position = int(new_position)
                
                role_to_move = discord.utils.get(atlanta.roles, id=role_id)
                if role_to_move:
                    await role_to_move.edit(position=new_position)
                    print(f"Moved role {role_to_move.name} to position {new_position}")
                    
                    # Return the updated role positions
                    roles = atlanta.roles
                    sorted_roles = sorted(roles, key=lambda x: x.position, reverse=True)
                    pos_list = {role.name: role.position for role in sorted_roles}
                    print("Updated role positions:")
                    print(pos_list)
                else:
                    print(f"Role with ID {role_id} not found.")
            else:
                print("Invalid number of arguments for 'rearrange' command.")
        else:
            print("Unknown command")
    except Exception as e:
        print(f"An error occured while trying to run command. {e}")"""

"""
async def handle_input():
   while True:
      command = input(f">> ")
      if command.lower() == "exit":
         break
      try:
          parts = command.split(" ")
          action = parts[0]
          args = parts[1:]

          await cmd_exc(action=action, *args)
      except Exception as e:
          print(f"An error occured when calling cmd_exc: {e}")
"""


if __name__ == "__main__":
    bot.run(get_token())