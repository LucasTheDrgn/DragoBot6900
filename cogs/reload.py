from re import compile,I

match = compile("^reload$",I).match

name = "reload"
form = "reload"
desc = "Reloads the bot, updating the settings and reloading any command modules"

admin = True

async def exec(cmd,msg,bot):
    if bot.auth(msg):
        await bot.reply("Got it!",msg,True)
        bot.reload()
    else:
        await bot.reply("Sorry, you're not authorized to use that command!",msg,True)