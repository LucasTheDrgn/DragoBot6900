from re import compile,I

match = compile("^help ?(\w+)?$",I).match

name = "help"
form = "help [command]"
desc = "Gives you help. \"help\" lists commands while \"help (command)\" gives you a description of that command."

async def exec(cmd,msg,bot):
    topic, = match(cmd).groups()
    if topic is None:
        commands = [cog.name for cog in filter(lambda x: not getattr(x,"hidden",False),bot.commands)]
        await bot.pm("These are the commands I know: ```"+"\n".join(commands)+"``` For more information, use `help (command)`",msg.author)
        return
    else:
        for cog in bot.commands:
            if cog.name == topic:
                res = ["```md\ncommand: "]
                res.append(cog.name)
                res.append("\nformat: ")
                res.append(cog.form)
                res.append("\ndescription: ")
                res.append(cog.desc)
                if getattr(cog,"admin",False):
                    res.append("\n**(admin only)**")
                if getattr(cog,"whitelist",False):
                    res.append("\n**(whitelist only)**")
                if getattr(cog,"hidden",False):
                    res.append("\n**(secret command)**")
                res.append("```")
                await bot.pm("".join(res),msg.author)
                return
        await bot.pm("Command not found. try `help` for a list of commands.",msg.author)
        return
