import inflect
inf = inflect.engine()

def make_mention(ctx):
	if ctx.guild is None:
		return ""
	else:
		return "{0}, ".format(ctx.author.mention)