"""my love isn't joke."""
import logging
from art import *
from pyrogram import *
from clear import clear

clients,clients_data=[],{}
def add_client(client):
  global clients,clients_data
  if client not in clients:
    clients.append(client)

async def start_all():
  global clients_data
  for client in clients:
    await client.start()
    clients_data[client.me.id] = {"client": client, "privilege": f"{'sudo' if client == clients[0] else 'user'}"}
  from Essentials.vars import AutoJoinChats, Support
  for app in clients:
    for i in AutoJoinChats:
      try: await app.join_chat(i)
      except: pass
  z,x,c=clear(),print(text2art("HazelUB"), end=""),logging.info("You're all set!")
  try: await clients[0].send_message(Support,"Up!")
  except: pass
  from Hazel.plugins.whatsapp import start_wa
  await start_wa()
  await idle()

"you.. is my world"