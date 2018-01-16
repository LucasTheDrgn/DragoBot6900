from re import compile,I

match = compile("^shutdown$",I).match

name = "shutdown"
form = "shutdown"
desc = "Shuts the bot down, closing out the program"

admin = True

async def exec(cmd,msg,bot):
    if bot.auth(msg):
        await bot.reply("Got it, shutting down!",msg,True)
        await bot.client.logout()
    else:
        await bot.reply("Sorry, you're not authorized to use that command!",msg,True)