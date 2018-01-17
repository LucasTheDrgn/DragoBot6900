from re import compile,I

match = compile("^hello$",I).match

name = "hello"
form = "hello"
desc = "Just saying hi!"

async def exec(cmd,msg,bot):
    await bot.reply("Hello!",msg,True)