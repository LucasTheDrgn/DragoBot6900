from re import compile,I
from random import randint

match = compile(r"^roll2 (?:1d)?(\d+)\+(?:1d)(\d+)$",I).match

name = "roll2"
form = "roll2 [1d](amount)+[1d](amount)"
desc = "Roll two dice of different sizes and add the result"

async def exec(cmd,msg,bot):
    a,b = match(cmd).groups()
    rolla = randint(1,int(a))
    rollb = randint(1,int(b))
    res = ", you rolled: {}+{}={}".format(rolla,rollb,rolla+rollb)
    await bot.reply(res,msg,True)

