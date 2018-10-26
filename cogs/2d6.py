from re import compile,I
from random import randint

match = compile(r"^2d6([+-]\d+)?$",I).match

name = "2d6"
form = "2d6[+|-modifier]"
desc = "Roll 2d6, with an optional modifier. Shortcut for !roll 2d6"

async def exec(cmd,msg,bot):
    mod = match(cmd).groups()
    amt = 2
    face = 6
    rolls = list()
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

