#!/usr/bin/env python3
import discord, json, asyncio, re
from importlib import reload

class Dragobot:

    def __init__(self):
        with open("keys.json") as f:
            self.keys = json.load(f)
        try:
            with open("memory.json") as f:
                self.memory = json.load(f)
        except FileNotFoundError:
            self.memory = dict()
        try:
            with open("settings.json") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            with open("default_settings.json") as f:
                with open("settings.json","w") as y:
                    y.write(f.read())
            with open("settings.json") as f:
                self.settings = json.load(f)

        self.commands = list()
        cog_re = re.compile(r"^(?P<path>(?:[^.]+\.)+)?(?P<cog>[^.]+)$")
        for cog in self.settings["extensions"]:
            m = cog_re.match(cog)
            if m is None:
                print("Missing cog: "+cog)
                continue
            path, ext = m.groups()
            if path is None:
                self.commands.append(__import__(ext))
            else:
                _temp = __import__(path[:-1],fromlist=[ext])
                self.commands.append(getattr(_temp,ext))
        
        self.client = discord.Client()

        @self.client.event
        async def on_message(message):
            await self.handle(message)

    async def handle(self,msg):
        for prefix in self.settings["prefix"]:
            m = re.match(prefix+"(?P<command>.*)",msg.content,re.I)
            if m:
                await self.command(m.group("command"),msg)

    async def command(self,cmd,msg):
        for cm in self.commands:
            if(cm.match(cmd)):
                print(("Command from "+msg.author.name+": "+cmd).encode(encoding="charmap",errors="replace").decode())

                if not self.auth(cmd,msg):
                    print("Unauthorized")
                    await bot.reply("Sorry, you're not authorized to use that command!",msg,True)
                    return

                if not self.whitelist(cmd,msg):
                    print("Server not whitelisted")
                    return

                await cm.exec(cmd,msg,self)
                return
        print(("Unknown command from "+msg.author.name+": "+cmd).encode(encoding="charmap",errors="replace").decode())

    async def reply(self,text,msg,mention=False):
        if(mention):
            text = msg.author.mention+" "+text
        await self.client.send_message(msg.channel,text)

    async def react(self,emoji,msg):
        await self.client.add_reaction(msg,emoji)

    async def pm(self,text,user):
        await self.client.send_message(user,text)

    def whitelist(self,cog,msg):
        if getattr(cog,"whitelist",False):
            if "whitelist" not in self.memory:
                return False
            if cog.name not in self.memory["whitelist"]:
                return False
            if msg.server.id not in self.memory["whitelist"][cog.name]:
                return False
        return True

    def run(self):
        print("Starting")
        self.client.run(self.keys["bot_token"])
        print("Cleaning up")
        self.cleanup()

    def cleanup(self):
        with open("memory.json","w") as f:
            json.dump(self.memory,f,indent=4)

    def reload(self):
        oldext = self.settings["extensions"]

        with open("settings.json") as f:
            self.settings = json.load(f)

        rm = list()

        for cog in self.commands:
            if cog.__name__ not in self.settings["extensions"]:
                rm.append(cog)
                continue
            try:
                reload(cog)
            except AttributeError:
                rm.append(cog)

        for cog in rm:
            self.commands.remove(cog)

        cog_re = re.compile(r"^(?P<path>(?:[^.]+\.)+)?(?P<cog>[^.]+)$")

        for cog in self.settings["extensions"]:
            if cog in oldext:
                continue
            m = cog_re.match(cog)
            if m is None:
                print("Missing cog: "+cog)
                continue
            path, ext = m.groups()
            if path is None:
                self.commands.append(__import__(ext))
            else:
                _temp = __import__(path[:-1],fromlist=[ext])
                self.commands.append(getattr(_temp,ext))

        print([cog.name for cog in self.commands])

    def auth(self,cog,msg):
        if getattr(cog,"admin",False):
            if msg.server:
                if msg.author.top_role >= msg.server.me.top_role:
                    return True
            sv = self.settings["supervisors"]
            for usr in sv:
                if msg.author.name == usr["name"] and int(msg.author.discriminator) == usr["discriminator"]:
                    return True
            return False
        return True

db = Dragobot()
db.run()