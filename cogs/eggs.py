from re import compile,I
from random import random

match = compile("^how many eggs\??$",I).match

name = "eggs"
form = "how many eggs[?]"
desc = "Well, how many?"

hidden = True

async def exec(cmd,msg,bot):
    count = 0
    while random()<0.75:
        count += 1
    await bot.reply(str(count)+".",msg,True)