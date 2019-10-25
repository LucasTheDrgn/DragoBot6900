from discord.ext import commands, tasks
import discord
from .util import checks, language, primatives
import youtube_dl
import typing

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
	'format': 'bestaudio/best',
	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
	'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)

		self.data = data

		self.title = data.get('title')
		self.url = data.get('url')

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]

		filename = data['url'] if stream else ytdl.prepare_filename(data)
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Voice(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.song_queue = primatives.defdict(default=lambda k: [])
		self.playing_queue = primatives.defdict(default=False)
		self.lastchannel = dict()
		self.playnext.start()

	def cog_unload(self):
		self.playnext.cancel()

	async def cog_before_invoke(self,ctx):
		self.lastchannel[ctx.guild.id] = ctx.channel

	@commands.command()
	async def join(self,ctx):
		if ctx.author.voice and ctx.author.voice.channel:
			if ctx.voice_client:
				await ctx.voice_client.move_to(ctx.author.voice.channel)
				src = discord.FFmpegPCMAudio("audio/cry.mp3")
				src = discord.PCMVolumeTransformer(src)
				src.volume = self.bot.memory[ctx.guild.id,"voice","volume"]
				ctx.voice_client.play(src)
				await ctx.send("{0}Moving over!".format(language.make_mention(ctx)))
			else:
				vc = await ctx.author.voice.channel.connect()
				src = discord.FFmpegPCMAudio("audio/cry.mp3")
				src = discord.PCMVolumeTransformer(src)
				src.volume = self.bot.memory[ctx.guild.id,"voice","volume"]
				vc.play(src)
				await ctx.send("{0}Will do!".format(language.make_mention(ctx)))
		else:
			await ctx.send("{0}You must be in a voice channel to use this command!".format(language.make_mention(ctx)))

	@commands.command()
	async def leave(self,ctx):
		if ctx.voice_client.is_connected():
			await ctx.voice_client.disconnect()
			await ctx.send("{0}Alright, have fun!".format(language.make_mention(ctx)))
		else:
			await ctx.send("{0}I'm not in a voice channel!".format(language.make_mention(ctx)))

	@commands.command()
	async def speak(self,ctx):
		vc = ctx.voice_client
		if vc:
			src = discord.FFmpegPCMAudio("audio/cry.mp3")
			src = discord.PCMVolumeTransformer(src)
			src.volume = self.bot.memory[ctx.guild.id,"voice","volume"]
			vc.play(src)
		else:
			await ctx.send("{0}I need to be in a voice channel to use this command!".format(language.make_mention(ctx)))

	@commands.command()
	async def yt(self, ctx, *, url):
		"""Plays from a url (almost anything youtube_dl supports)

		A list of supported sites can be found here: https://ytdl-org.github.io/youtube-dl/supportedsites.html"""

		async with ctx.typing():
			player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=False)
			player.volume = self.bot.memory[ctx.guild.id,"voice","volume"]
			ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
			
		await ctx.send('{0}Now playing: {1}'.format(language.make_mention(ctx),player.title))

	@commands.group(invoke_without_command=True)
	async def queue(self,ctx, url: typing.Optional[str]):
		"""Enqueues from a url (almost anything youtube_dl supports)

		A list of supported sites can be found here: https://ytdl-org.github.io/youtube-dl/supportedsites.html"""
		if url:
			async with ctx.typing():
				player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=False)
				self.song_queue[ctx.guild.id].append(player)
				self.playing_queue[ctx.guild.id] = True

			if ctx.voice_client.is_playing():
				await ctx.send('{0}Queued: {1} at position {2}'.format(language.make_mention(ctx),player.title,len(self.song_queue[ctx.guild.id])))
			#else:
				#await ctx.send('{0}Now playing: {1}'.format(language.make_mention(ctx),player.title))
		else:
			dispqueue = []
			if len(self.song_queue[ctx.guild.id]) == 0 and not ctx.voice_client.is_playing():
				await ctx.send("{0}No songs currently queued!".format(language.make_mention(ctx)))
				return
			elif len(self.song_queue[ctx.guild.id]) > 10:
				for i in range(10):
					dispqueue.append("{0}: {1}".format(i+1,self.song_queue[ctx.guild.id][i].title))
				output = "{0}Currently {1} items in queue (only displaying next 10): ```{2}```"
			else:
				for i in range(len(self.song_queue[ctx.guild.id])):
					dispqueue.append("{0}: {1}".format(i+1,self.song_queue[ctx.guild.id][i].title))
				output = "{0}Currently {1} items in queue: ```{2}```"
			if ctx.voice_client.is_playing() and hasattr(ctx.voice_client.source,"title"):
				dispqueue.insert(0,"Now playing: {0}".format(ctx.voice_client.source.title))

			await ctx.send(output.format(language.make_mention(ctx),len(self.song_queue[ctx.guild.id]),"\n".join(dispqueue)))

	@queue.command()
	async def play(self,ctx):
		if ctx.voice_client.is_paused():
			ctx.voice_client.resume()
			return
		elif ctx.voice_client.is_playing():
			await ctx.send("{0}I'm already playing something! Please stop that first.".format(language.make_mention(ctx)))
			return
		else:
			self.playing_queue[ctx.guild.id] = True

	@queue.command()
	async def skip(self,ctx,amount: typing.Optional[int]):
		if amount is None:
			await ctx.send("{0}Skipping song...".format(language.make_mention(ctx)))
			ctx.voice_client.stop()
			#if ctx.voice_client.is_playing():
				#await ctx.send('{0}Now playing: {1}'.format(language.make_mention(ctx),ctx.voice_client.source.title))
			return
		elif amount-1 >= len(self.song_queue[ctx.guild.id]):
			await ctx.send("{0}Skipping entire queue...".format(language.make_mention(ctx)))
			self.song_queue[ctx.guild.id] = []
			self.playing_queue[ctx.guild.id] = False
			ctx.voice_client.stop()
			return
		else:
			await ctx.send("{0}Skipping this and {1} other songs...".format(language.make_mention(ctx),amount-1))
			self.song_queue[ctx.guild.id] = self.song_queue[ctx.guild.id][amount-1:]
			ctx.voice_client.stop()

	@commands.command()
	async def stop(self,ctx):
		if ctx.voice_client.is_playing():
			ctx.voice_client.stop()
		else:
			await ctx.send("{0}I'm not playing anything!".format(language.make_mention(ctx)))
			return

	@commands.command()
	async def pause(self,ctx):
		if ctx.voice_client.is_playing():
			ctx.voice_client.pause()
		else:
			await ctx.send("{0}I'm not playing anything!".format(language.make_mention(ctx)))
			return

	@commands.command()
	async def play(self,ctx):
		if ctx.voice_client.is_paused():
			ctx.voice_client.resume()
		else:
			await ctx.send("{0}I don't have anything paused!".format(language.make_mention(ctx)))
			return

	@commands.command()
	async def volume(self,ctx,volume: typing.Optional[int]):
		if volume:
			if ctx.voice_client and ctx.voice_client.source and hasattr(ctx.voice_client.source,"volume"):
				ctx.voice_client.source.volume = volume/100
			self.bot.memory[ctx.guild.id,"voice","volume"] = volume/100
			await ctx.send("{0}Volume set to {1}%".format(language.make_mention(ctx),volume))
		else:
			await ctx.send("{0}Volume is at {1}%".format(language.make_mention(ctx),int(self.bot.memory[ctx.guild.id,"voice","volume"]*100)))

	@tasks.loop(seconds=5.0)
	async def playnext(self):
		for vc in self.bot.voice_clients:
			if vc.guild and self.playing_queue[vc.guild.id] and not vc.is_playing():
				if len(self.song_queue[vc.guild.id]) > 0:
					nextpl = self.song_queue[vc.guild.id].pop(0)
					nextpl.volume = self.bot.memory[vc.guild.id,"voice","volume"]
					vc.play(nextpl, after=lambda e: print('Player error: %s' % e) if e else None)
					await self.lastchannel[vc.guild.id].send('Now playing: {0}'.format(nextpl.title))
				else:
					self.playing_queue[vc.guild.id] = False

def setup(bot):
	bot.add_cog(Voice(bot))