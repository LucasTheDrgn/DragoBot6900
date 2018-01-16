from re import compile,I
from random import randint

match = compile(r"^roll (\d+)d(\d+)([+-]\d+)?$",I).match

name = "roll"
form = "roll (amount)d(faces)[+|-modifier]"
desc = "Roll some amount of dice and have the bot count it up for you"

async def exec(cmd,msg,bot):
    amt, face, mod = match(cmd).groups()
    rolls = list()
    face = int(face)
    for _ in range(int(amt)):
        rolls.append(randint(1,face))
    res = ", you rolled: "
    if len(rolls) == 1:
        res += str(rolls[0])
        if mod:
            res += mod+"="+str(rolls[0]+int(mod))
    else:
        res += repr(rolls)+(mod or "")+"="+str(sum(rolls)+int(mod or 0))
    await bot.reply(res,msg,True)

