from sys import argv
from hashlib import md5
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from itertools import chain,repeat
from re import compile,I
from requests import get
from io import BytesIO

match = compile(r"^palettize ?(.*)$",I).match

name = "palettize"
form = "palettize [input]"
desc = "Turn a phrase into a palette! Also accepts files! Uses md5 hashes!"

async def exec(cmd,msg,bot):
   
    if msg.attachments:
        data = b''
        for at in msg.attachments:
            r = get(at['url'])
            data += r.content
    else:
        data = bytes(match(cmd).group(1),'utf-8')

    m = md5()
    m.update(data)
    hsh = m.digest()

    img = Image.new("RGB",(360,240),color=None)

    cols = list()
    for i in range(0,15,3):
        cols.append((hsh[i],hsh[i+1],hsh[i+2]))

    imgdata = list(chain.from_iterable(map(lambda x: [x]*72,cols)))*240
    img.putdata(imgdata)

    drw = ImageDraw.Draw(img)

    font_colors = list()
    for c in cols:
        font_colors.append(tuple([(v+128)%256 for v in c]))

    font = ImageFont.truetype("assets/consola.ttf",size=12)

    for i in range(5):
        text = "#{:02x}{:02x}{:02x}".format(*cols[i])

        anch = (i*72+36,230)
        size = font.getsize(text)
        pos = (anch[0]-size[0]/2,anch[1]-size[1])

        drw.text(pos,text,font_colors[i],font)

    b = BytesIO()
    img.save(b,"PNG")
    b.seek(0)
    b.name = "palette.png"

    await bot.reply_file("",b,msg,True)
