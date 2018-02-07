from re import compile,I
from random import choice

match = compile(r"^8ball$",I).match

name = "8ball"
form = "8ball"
desc = "Ask the magic 8 ball for an answer... (might be a little biased)"

async def exec(cmd,msg,bot):
    await bot.reply(choice(bot.settings["8ball"]),msg,True)
