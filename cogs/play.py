from re import compile,I
from discord import Game

match = compile("^play( .+)?$",I).match

name = "play"
form = "play (game)"
desc = "Sets the bot's 'playing' status to the specified game"

admin = True

async def exec(cmd,msg,bot):
    if bot.auth(msg):
        game, = match(cmd).groups()
        if game:
            await bot.client.change_presence(game=Game(name=game.strip()))
        else:
            await bot.client.change_presence()
    else:
        await bot.reply("Sorry, you're not authorized to use that command!",msg,True)