from discord.ext import commands
import discord
from .util import checks, language

class Basics(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def hello(self,ctx):
		"""Say hello!"""
		await ctx.send("{0}Hello!".format(language.make_mention(ctx)))

	@commands.command(hidden=True)
	@commands.is_owner()
	async def shutdown(self,ctx):
		"""Shut the bot down"""
		await ctx.send("{0}Got it! Shutdown initiated!".format(language.make_mention(ctx)))
		await self.bot.logout()

class Administration(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command(
		help=
		"""Add or remove supervisors from your server.

		Usable only by server owners or the bot's owner""",
		usage="[add/remove] [any number of user or role mentions]")
	@checks.has_atleast_level(4)
	async def supervisor(self,ctx,*args):
		guildid = ctx.guild.id
		sv = ctx.bot.memory[guildid]["supervisors"]
		sr = ctx.bot.memory[guildid]["supervisor_roles"]
		svl = len(sv)
		srl = len(sr)
		if len(args) > 0:
			if args[0].lower() == "add":
				for member in ctx.message.mentions:
					if member.id not in sv:
						sv.append(member.id)
				for role in ctx.message.role_mentions:
					if role.id not in sr:
						sr.append(role.id)
			elif args[0].lower() == "remove":
				for member in ctx.message.mentions:
					while member.id in sv:
						sv.remove(member.id)
				for role in ctx.message.role_mentions:
					while role.id in sr:
						sr.remove(role.id)
			else:
				await ctx.send("{0}Please specify if you're adding or removing supervisors.".format(language.make_mention(ctx)))
				return
		else:
			await ctx.send("{0}Please specify if you're adding or removing supervisors.".format(language.make_mention(ctx)))
			return

		flags = [
			len(ctx.message.mentions)!=0,
			len(ctx.message.role_mentions)!=0,
			len(sv)!=svl,
			len(sr)!=srl
		]
		if args[0].lower() == "add":
			if not (flags[0] or flags[1]):
				await ctx.send("{0}No changes requested.".format(language.make_mention(ctx)))
				return
			if flags[2]:
				if flags[3]:
					await ctx.send("{0}Added {1} {2} and {3} supervisor {4}.".format(language.make_mention(ctx),len(sv)-svl,language.inf.plural("supervisor",len(sv)-svl),len(sr)-srl,language.inf.plural("role",len(sr)-srl)))
					return
				else:
					if flags[1]:
						await ctx.send("{0}Added {1} {2}. No changes needed to supervisor roles.".format(language.make_mention(ctx),len(sv)-svl,language.inf.plural("supervisor",len(sv)-svl)))
						return
					else:
						await ctx.send("{0}Added {1} {2}.".format(language.make_mention(ctx),len(sv)-svl,language.inf.plural("supervisor",len(sv)-svl)))
						return
			else:
				if flags[3]:
					if flags[0]:
						await ctx.send("{0}Added {1} supervisor {2}. No changes needed to supervisors.".format(language.make_mention(ctx),len(sr)-srl,language.inf.plural("role",len(sr)-srl)))
						return
					else:
						await ctx.send("{0}Added {1} supervisor {2}.".format(language.make_mention(ctx),len(sr)-srl,language.inf.plural("role",len(sr)-srl)))
						return
				else:
					await ctx.send("{0}No changes needed.".format(language.make_mention(ctx)))
					return
		elif args[0].lower() == "remove":
			if not (flags[0] or flags[1]):
				await ctx.send("{0}No changes requested.".format(language.make_mention(ctx)))
				return
			if flags[2]:
				if flags[3]:
					await ctx.send("{0}Removed {1} {2} and {3} supervisor {4}.".format(language.make_mention(ctx),svl-len(sv),language.inf.plural("supervisor",svl-len(sv)),srl-len(sr),language.inf.plural("role",srl-len(sr))))
					return
				else:
					if flags[1]:
						await ctx.send("{0}Removed {1} {2}. No changes needed to supervisor roles.".format(language.make_mention(ctx),svl-len(sv),language.inf.plural("supervisor",svl-len(sv))))
						return
					else:
						await ctx.send("{0}Removed {1} {2}.".format(language.make_mention(ctx),svl-len(sv),language.inf.plural("supervisor",svl-len(sv))))
						return
			else:
				if flags[3]:
					if flags[0]:
						await ctx.send("{0}Removed {1} supervisor {2}. No changes needed to supervisors.".format(language.make_mention(ctx),srl-len(sr),language.inf.plural("role",srl-len(sr))))
						return
					else:
						await ctx.send("{0}Removed {1} supervisor {2}.".format(language.make_mention(ctx),srl-len(sr),language.inf.plural("role",srl-len(sr))))
						return
				else:
					await ctx.send("{0}No changes needed.".format(language.make_mention(ctx)))
					return

	@commands.command(
		help=
		"""Add or remove a prefix from your server.

		Dragobot will always respond to "dragobot, ", but with this command you can add or remove other prefixes for him to respond to.

		Usable by any bot supervisors""",
		usage="[add/remove] [prefix]")
	@checks.has_atleast_level(2)
	async def prefix(self,ctx,addremove: str, prefix: str):
		if addremove == "add":
			if prefix not in self.bot.memory[ctx.guild.id]["prefixes"]:
				self.bot.memory[ctx.guild.id]["prefixes"].append(prefix)
				await ctx.send("{0}Got it! I will now respond to \"{1}\".".format(language.make_mention(ctx),prefix))
				return
			else:
				await ctx.send("{0}I was already responding to \"{1}\"!".format(language.make_mention(ctx),prefix))
				return
		elif addremove == "remove":
			if prefix in self.bot.memory[ctx.guild.id]["prefixes"]:
				while prefix in self.bot.memory[ctx.guild.id]["prefixes"]:
					self.bot.memory[ctx.guild.id]["prefixes"].remove(prefix)
				await ctx.send("{0}Got it! I will no longer respond to \"{1}\".".format(language.make_mention(ctx),prefix))
				return
			else:
				await ctx.send("{0}I already wasn't responding to \"{1}\"!".format(language.make_mention(ctx),prefix))
				return



def setup(bot):
	bot.add_cog(Basics(bot))
	bot.add_cog(Administration(bot))
