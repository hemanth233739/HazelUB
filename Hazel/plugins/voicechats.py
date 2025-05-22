from .. import *
from pyrogram import *
from MultiSessionManagement import *

@on_message(filters.command('joinvc', prefixes=HANDLER)&filters.me&filters.group)
async def joinvc(c,m):
  pytgcalls_client = clients_data[c.me.id]["pytgcalls_client"]
  await pytgcalls_client.play(m.chat.id)
  await m.reply("Okay, i've joined in vc.")
  
@on_message(filters.command('leavevc', prefixes=HANDLER)&filters.me&filters.group)
async def leavevc(c,m):
  pytgcalls_client = clients_data[c.me.id]["pytgcalls_client"]
  await pytgcalls_client.leave_call(m.chat.id)
  await m.reply("left from the vc.")  