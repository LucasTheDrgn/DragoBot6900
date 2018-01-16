from re import compile,I

match = compile(r"^pronouns ((?:get)|(?:set)) (.+)",I).match

name = "pronouns"
form = "pronouns (get|set) (pronouns|user)"
desc = "Tell the bot which pronouns you use, or ask the bot what pronouns someone else uses"

async def exec(cmd,msg,bot):
    opt,val = match(cmd).groups()
    if("pronouns" not in bot.memory):
        bot.memory["pronouns"] = dict()
    if opt == "set":
        bot.memory["pronouns"][msg.author.id] = val
        await bot.reply("Got it, your pronouns are "+val,msg,True)
        return
    if opt == "get":
        if len(msg.mentions)>0:
            mnt = msg.mentions[0].id
        else:
            if msg.server is None:
                await bot.reply("I'm having trouble finding them, make sure you're spelling their name right or we're in a server with them!",msg,True)
                return
            if val[1] == "@":
                val = val[1:]
            usr = msg.server.get_member_named(val)
            if usr is None:
                await bot.reply("I'm having trouble finding them, make sure you're spelling their name right or we're in a server with them!",msg,True)
                return
            mnt = usr.id
        if mnt in bot.memory["pronouns"]:
            await bot.reply("They use "+bot.memory["pronouns"][mnt]+" pronouns",msg,True)
        else:
            await bot.reply("I'm not sure, you should ask them!",msg,True)