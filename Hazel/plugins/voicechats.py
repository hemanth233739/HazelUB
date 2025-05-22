from .. import *
from pyrogram import *
from MultiSessionManagement import *

@on_message(filters.command('joinvc', prefixes=HANDLER)&filters.me)
async def joinvc(c,m):
  pytgcalls_client = clients_data[c.me.id]["pytgcalls_client"]
  await pytgcalls_client.play(m.chat.id)
  await m.reply("Okay, i've joined in vc.")