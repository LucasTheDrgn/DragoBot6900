#!/usr/bin/env python3
import json, asyncio, re, os
from discord.ext import commands
from discord.opus import load_opus
from importlib import import_module

def makesafe(object):
    return str(object).encode(encoding="charmap",errors="replace").decode()

def safeprint(*objects,**kwargs):
    return print(*map(makesafe,objects),**kwargs)

def blacklist(ctx):
    if ctx.guild is None:
        return True
    if ctx.invoked_with in ctx.bot.memory[ctx.guild.id]["blacklist"]:
        return False
    if "channel_whitelist" in ctx.bot.memory[ctx.guild.id] and ctx.channel.id not in ctx.bot.memory[ctx.guild.id]["channel_whitelist"]:
        return False
    if "channel_blacklist" in ctx.bot.memory[ctx.guild.id] and ctx.channel.id in ctx.bot.memory[ctx.guild.id]["channel_blacklist"]:
        return False
    return True

class Dragobot(commands.Bot):
    def __init__(self,*args,**kwargs):
        kwargs["command_prefix"] = self.get_prefix
        super().__init__(*args,**kwargs)

        self.memory = dict()

        for fn in os.listdir("extensions"):
            if fn != '__init__.py' and fn[-3:] == '.py':
                self.load_extension("extensions.{0}".format(fn[:-3]))

        print("Loaded {0} extensions:".format(len(self.extensions)))
        for ext in self.extensions:
            print("\t{0}".format(ext))

        self.check(blacklist)

    def memory_load(self,id):
        if id in self.memory:
            return
        try:
            with open("memory/{0}.json".format(id)) as f:
                self.memory[id] = json.load(f)
        except FileNotFoundError:
            with open("default_settings.json") as f:
                self.memory[id] = json.load(f)

    async def get_prefix(self,message):
        if message.guild is None:
            return ["dragobot, ",""]

        if message.guild.id in self.memory:
            if "prefixes" in self.memory[message.guild.id]:
                return ["dragobot, "]+self.memory[message.guild.id]["prefixes"]

        return "dragobot, "

    async def close(self):
        exts = list(self.extensions.keys())
        print("Unloading {0} extensions:".format(len(exts)))
        for ext in exts:
            print("\t{0}".format(ext))
            self.unload_extension(ext)
        print("Saving memory for {0} guilds:".format(len(self.memory)))
        for guild in self.memory:
            print("\t{0}".format(guild))
            with open("memory/{0}.json".format(guild),"w") as f:
                json.dump(self.memory[guild],f,indent=4)
        print("Complete")
        await super().close()

    async def on_ready(self):
        safeprint("Logged in as {0} ({0.id}) connected to {1} guilds.".format(self.user,len(self.guilds)))
        for g in self.guilds:
            safeprint("\t{0.name}: {0.id}".format(g))
            self.memory_load(g.id)

    async def on_guild_join(self,guild):
        self.memory_load(guild.id)

with open("token.txt") as f:
    token = f.read()

db = Dragobot()

try:
    db.run(token)
except KeyboardInterrupt:
    print("Keyboard interrupt recieved by console. Shutting down.")