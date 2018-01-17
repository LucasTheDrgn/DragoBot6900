from re import compile,I

match = compile(r"^whitelist ((?:add)|(?:remove)) (.+)",I).match

name = "whitelist"
form = "whitelist (add|remove) (command)"
desc = "Add or remove a command from the server's whitelist. You can add or remove any commands you want, but only commands programmed to be whitelisted will be affected."

admin = True

async def exec(cmd,msg,bot):
    opt,val = match(cmd).groups()
    if "whitelist" not in bot.memory:
        bot.memory["whitelist"] = dict()
    if opt == "add":
        if val not in bot.memory["whitelist"]:
            bot.memory["whitelist"][val] = list()
        bot.memory["whitelist"][val].append(msg.server.id)
        await bot.reply("Got it, the command "+val+" is now whitelisted here.",msg,True)
        return
    if opt == "remove":
        if val not in bot.memory["whitelist"]:
            await bot.reply("That command was never whitelisted here!",msg,True)
            return
        if msg.server.id not in bot.memory["whitelist"][val]:
            await bot.reply("That command was never whitelisted here!",msg,True)
            return
        bot.memory["whitelist"][val].remove(msg.server.id)
        await bot.reply("Got it, the command "+val+" is no longer whitelisted here.",msg,True)
        return