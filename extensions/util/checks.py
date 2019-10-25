from discord.ext import commands

def has_atleast_level(level):
	"""Levels are as follows:
	0 - Unprivileged user. Don't bother with a check for this level.
	1 - User has a role above the bot
	2 - User has a role in the 'supervisor_roles' list
	3 - User is in the 'supervisors' list
	4 - Server owner
	5 - Bot owner only. Use is_owner for checking this level."""
	def predicate(ctx):
		if ctx.guild is None:
			if level > 0:
				raise commands.NoPrivateMessage("This command requires certain privileges. Please use from within the relevant server.")
			else:
				raise commands.NoPrivateMessage("This command requires you use it from within a server.")

		guildid = ctx.guild.id
		if ctx.bot.is_owner(ctx.author):
			return True
		if ctx.author == ctx.guild.owner:
			return level <= 4
		if ctx.author.id in ctx.bot.memory[guildid,"supervisors"]:
			return level <= 3
		if len(set(map(lambda x: x.id,ctx.author.roles)).intersection(ctx.bot.memory[guildid,"supervisor_roles"]))>0:
			return level <= 2
		if ctx.author.top_role > ctx.me.top_role:
			return level <= 1
		return level <= 0
	return commands.check(predicate)

def whitelist_required():
	def predicate(ctx):
		return ctx.invoked_with in ctx.bot.memory[ctx.guild.id,"whitelist"]
	return commands.check(predicate)