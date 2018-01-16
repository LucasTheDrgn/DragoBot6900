from re import compile,I

match = compile("^validate me$",I).match

name = "valid"
form = "validate me"
desc = "If you need validation, YOU \U0001F44F ARE \U0001F44F VALID \U0001F44F"

async def exec(cmd,msg,bot):
    await bot.react("\U0001f1fa",msg)
    await bot.react("\U0001f1f7",msg)
    await bot.react("\U0001f1fb",msg)
    await bot.react("\U0001f1e6",msg)
    await bot.react("\U0001f1f1",msg)
    await bot.react("\U0001f1ee",msg)
    await bot.react("\U0001f1e9",msg)