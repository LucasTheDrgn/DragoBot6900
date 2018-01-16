from re import compile,I

match = compile("^whoami$",I).match

name = "whoami"
form = "whoami"
desc = "Asks the bot to give you any information it has on you (responds in pm)"

async def exec(cmd,msg,bot):
    info = list()
    aut = msg.author
    info.append("username: ")
    info.append(aut.name)
    info.append("discriminator: ")
    info.append(aut.discriminator)
    info.append("id: ")
    info.append(aut.id)
    info.append("avatar url:")
    info.append(aut.avatar_url)
    info.append("display name:")
    info.append(aut.display_name)
    info.append("creation time:")
    info.append(aut.created_at.isoformat(" "))
    if(hasattr(aut,"server")):
        info.append("server:")
        info.append(aut.server.name)
        info.append("joined at:")
        info.append(aut.joined_at.isoformat(" "))
        info.append("server nickname:")
        info.append(aut.nick)
        info.append("roles:")
        info.append([r.name for r in aut.roles])
        info.append("top role:")
        info.append(aut.top_role.name)
        if(aut.game):
            info.append("game:")
            info.append(aut.game.name)
            if(aut.game.type==1):
                info.append("stream url:")
                info.append(aut.game.url)
    await bot.pm("This is all the info I have on you: ```"+"\n".join(map(str,info))+"```",aut)