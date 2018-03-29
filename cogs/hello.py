from re import compile,I

match = compile("^hello$",I).match

name = "hello"
form = "hello"
desc = "Just saying hi!"

async def exec(cmd,msg,bot):
    if msg.attachments:
        print(msg.attachments)
    await bot.reply("Hello!",msg,True)