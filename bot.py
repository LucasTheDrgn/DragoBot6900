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
            if(msg.content.startswith(prefix)):
                await self.command(msg.content[len(prefix):],msg)

    async def command(self,cmd,msg):
        for cm in self.commands:
            if(cm.match(cmd)):
                print(("Command from "+msg.author.name+": "+cmd).encode(encoding="charmap",errors="replace").decode())
                await cm.exec(cmd,msg,self)
                return

    async def reply(self,text,msg,mention=False):
        if(mention):
            text = msg.author.mention+" "+text
        await self.client.send_message(msg.channel,text)

    async def pm(self,text,user):
        await self.client.send_message(user,text)

    def run(self):
        print("Starting")
        self.client.run(self.keys["bot_token"])
        print("cleanup")
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

    def auth(self,msg):
        if msg.server:
            if msg.author.top_role >= msg.server.me.top_role:
                return True
        sv = self.settings["supervisors"]
        for usr in sv:
            if msg.author.name == usr["name"] and int(msg.author.discriminator) == usr["discriminator"]:
                return True
        return False

db = Dragobot()
db.run()