from re import compile,I
from random import choice,randint

match = compile(r"^(8|e)ball.*$",I).match

name = "8ball"
form = "(8ball|eball) [question]"
desc = "Ask the magic 8 ball for an answer... (might be a little biased)"

async def exec(cmd,msg,bot):
    await bot.reply(choice(bot.settings["8ball"]),msg,True)
