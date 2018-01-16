from re import compile,I
from discord import ChannelType

match = compile("^voice (\w+) ?(.+)?$",I).match

name = "voice"
form = "voice list"
desc = "Lists the voice channels"

admin = True

player = None
volume = 1

async def exec(cmd,msg,bot):
    global player,volume
    subc,opt = match(cmd).groups()
    if bot.auth(msg):
        if subc == "list":
            await bot.reply(str([x.name for x in filter(lambda x: x.type == ChannelType.voice,msg.server.channels)]),msg,True)
            return
        if subc == "join":
            for chn in filter(lambda x: x.type == ChannelType.voice,msg.server.channels):
                if chn.name == opt:
                    vc = bot.client.voice_client_in(msg.server)
                    if vc:
                        await vc.move_to(chn)
                        return
                    else:
                        await bot.client.join_voice_channel(chn)
                        return
        if subc == "leave":
            vc = bot.client.voice_client_in(msg.server)
            if vc:
                await vc.disconnect()
        if subc == "play":
            if player and not player.is_done():
                player.resume()
                return
            vc = bot.client.voice_client_in(msg.server)
            if vc:
                player = vc.create_ffmpeg_player("media/"+opt)
                player.start()
                player.volume = volume
                return
        if subc == "yt":
            vc = bot.client.voice_client_in(msg.server)
            if vc:
                player = await vc.create_ytdl_player(opt)
                player.start()
                player.volume = volume
                return
        if subc == "pause":
            if player and player.is_playing():
                player.pause()
                return
        if subc == "stop":
            if player and not player.is_done():
                player.stop()
                return
        if subc == "volume":
            volume = int(opt)/10
            if player and not player.is_done():
                player.volume = volume
                return

    else:
        await bot.reply("Sorry, you're not authorized to use that command!",msg,True)