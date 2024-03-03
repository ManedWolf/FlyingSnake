import logging  # debug / info / warning / exception error / critical
import asyncio
import discord
from discord.ext import commands
import os

async def main():

  try:

    # Logging
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S', filename='./logs/logs.log', encoding='utf-8', level=logging.DEBUG)
    discord_log = logging.FileHandler(filename='./logs/discord.log', encoding='utf-8')

    # Discord Bot Intents
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=('/FS', '/fs', '/', ''), intents=intents)

    # Discord Client Event
    @bot.event
    async def on_ready():
      logging.info(f'Logged on as {bot.user}!')

    # On message
    @bot.event
    async def on_message(message):
      await bot.process_commands(message)
      #if message.author != client.user:
      #  check(message)

    # Loading Cogs
    for file in os.listdir('./cogs'):
      if file.endswith('.py'):
        await bot.load_extension(f'cogs.{file[:-3]}')

    # Bot Running
    with open('./token', 'r') as token:
      await bot.start(token.read())#, log_handler=discord_log, log_level=logging.DEBUG)
  
  except FileNotFoundError:
    logging.critical('main(): missing token file')

  except:
    logging.exception('main(): error during bot startup')

  return

asyncio.run(main())

"""
@client.event
async def on_message(message):
  if message.author != client.user:
    check(message)
    #await message.add_reaction('✅')
    #await message.channel.send(check(message.content))
"""