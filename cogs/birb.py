from re import compile,I

match = compile("^am I a pretty birb\?$",I).match

name = "birb"
form = "am I a pretty birb?"
desc = "Achieve validation"

hidden = True

async def exec(cmd,msg,bot):
    await bot.reply("Yes, very.",msg,True)