# IMPORTS

import os       # open close
import json     # load dump
import time     # time
import datetime # datetime.now
import logging  # debug / info / warning / exception/error / critical
import discord
from discord.ext import commands
from discord import app_commands

# COG

class Data(commands.Cog):

  # INITIALIZATION

  def __init__(self, bot):
    self.bot = bot
    self.ctxmenu_delete_all = app_commands.ContextMenu(
      name = 'Delete My Variables',
      callback = self.delete_all,
    )
    self.bot.tree.add_command(self.ctxmenu_delete_all)

  @commands.Cog.listener()
  async def on_ready(self):
    logging.info(f'{self.__class__.__name__}: cog loaded')
    #print([c.name for c in self.get_commands()])

  @commands.hybrid_command(description = "Synchronizes bot commands with discord servers")
  async def sync(self, ctx):
    syncing = await ctx.bot.tree.sync()
    logging.info(f'{self.__class__.__name__}: {len(syncing)} command(s) loaded')
    await ctx.send(f'{self.__class__.__name__}: {len(syncing)} command(s) loaded')
  

  #@app_commands.command(description = "Create or modify a variable.")
  #async def variables(self, interaction, variable:str, value:str):
  # Choice pour les variables ?

  #GetMyData récupère son fichier de variables ?


          









  

  # SETTING VARIABLES

  @app_commands.command(description = "Create or modify a variable.")
  async def set(self, interaction, variable:str, value:str):
    # NEED TO FORCE VARIABLE NAMES TO BE AZa-z_

    """ /set <variable> [value] (alias: /s /fss /fsset)
    Create or modify a variable while keeping a history of modifications.
    A variable name can only contain letters and underscores.
    Depending on the context, the value of a variable is interpreted as plain text or as an arithmetical expression.
    """

    if not variable:
      logging.error("Data.set(): variable name missing")
      await interaction.response.send_message("error: variable name missing", delete_after=5, ephemeral=True)
      return

    try:
      with open("data/"+str(interaction.user.id)+'.json', 'r+') as file:
        dump = json.load(file)
        if value != dump[variable]['history'][dump[variable]['version']] and value:
          dump[variable]['history'] = dump[variable]['history'][:dump[variable]['version']+1]
          dump[variable]['history'] += [{'value':value,'date':int(time.time())}]
          dump[variable]['version'] += 1

    except FileNotFoundError:
      logging.info("Data.set(): file missing")
      with open("data/"+str(interaction.user.id)+'.json', 'w+') as file:
        json.dump({variable:{"version":0,"history":[{"value":value,"date":int(time.time())}]}}, file, indent=2)

    except json.JSONDecodeError:
      logging.error("Data.set(): invalid JSON")
      flush(interaction.user.id)
      with open("data/"+str(interaction.user.id)+'.json', 'w+') as file:
        file.truncate()
        json.dump({variable:{"version":0,"history":[{"value":value,"date":int(time.time())}]}}, file, indent=2)

    except KeyError:
      dump[variable] = {"version":0,"history":[{"value":value,"date":int(time.time())}]}
      with open("data/"+str(interaction.user.id)+'.json', 'w+') as file:
        file.truncate()
        json.dump(dump, file, indent=2)

    except Exception as exception:
      logging.exception("Data.set(): "+exception)
      await interaction.response.send_message("error: unknown exception", ephemeral=True)

    await interaction.response.send_message(f"olala", ephemeral=True, delete_after=5)

  # DELETING ALL VARIABLES

  async def delete_all(self, interaction:discord.Interaction, message:discord.Message):

    """
    Delete all your variables.
    """

    try:
      with open(f"data/{str(interaction.user.id)}.json", 'r+') as file:
        variables = json.load(file)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for variable in variables.values():
          if variable['history'][variable['version']]:
            variable['history'] \
            = variable['history'][:variable['version']+1] \
            + variable['history'][len(variable['history'])-2:variable['version']-1:-1] \
            + [{'value':"",'date':timestamp}]
            variable['version'] = len(variable['history'])-1
        file.seek(0)
        file.truncate()
        json.dump(variables, file, indent=2)
        await interaction.response.send_message(f"All variables deleted", ephemeral=True, delete_after=3)

    except FileNotFoundError:
      logging.warning("Data.delete_all(): file missing")
      await interaction.response.send_message(f"No variable database detected, create a variable first.", ephemeral=True, delete_after=5)

    except Exception as exception:
      logging.exception(f"Data.delete_all(): {exception}")
      await interaction.response.send_message(f"Unknown exception: {exception}", ephemeral=True)






async def setup(bot):
  await bot.add_cog(Data(bot))