from pyrogram import *
from .. import *
from pyrogram.types import Message

db = DATABASE["safeEscrow"]

@on_message(filters.command(["aescrower"], prefixes=HANDLER) & filters.me)
async def add_escrower(c, m):
  client_id = c.me.id
  if not m.reply_to_message or not m.reply_to_message.from_user:
    return await m.reply("Reply to your escrower.")
  escrower = m.reply_to_message.from_user
  name = escrower.first_name + (f" {escrower.last_name}" if escrower.last_name else "")
  username = escrower.username or "None"
  lower_name = name.strip().lower()
  if await db.count_documents({"client_id": client_id, "escrowers.id": escrower.id}):
    return await m.reply("You've already registered them..")
  await db.update_one(
    {"client_id": client_id},
    {"$push": {"escrowers": {"id": escrower.id, "username": username.lower(), "name": lower_name}}},
    upsert=True
  )
  await m.reply(f"""
![✅](tg://emoji?id=5318840353510408444) **Registered!**
  ![👤](tg://emoji?id=5258011929993026890) **Name:** {lower_name}
  ![ℹ️](tg://emoji?id=4967518033061872209) **Userid:** `{escrower.id}`
  ![🙍](tg://emoji?id=5206413872231099655) **Username:** `{username}`""")

@on_message(filters.command(["rescrower"], prefixes=HANDLER) & filters.me)
async def remove_escrower_handler(c, m):
  client_id = c.me.id
  if not m.reply_to_message or not m.reply_to_message.from_user:
    return await m.reply("Reply to your escrower.")
  escrower = m.reply_to_message.from_user
  result = await db.update_one(
    {"client_id": client_id},
    {"$pull": {"escrowers": {"id": escrower.id}}}
  )
  if result.modified_count:
    return await m.reply("Done!")
  await m.reply("They haven't registered.")

#@on_message(~filters.me, group=10)
async def detect_clone(c, m: Message):
  client_id = c.me.id
  doc = await db.find_one({"client_id": client_id})
  if not doc or "escrowers" not in doc:
    return
  user = m.from_user
  name = user.first_name + (f" {user.last_name}" if user.last_name else "")
  username = user.username or "None"
  lower_name = name.strip().lower()
  for escrower in doc["escrowers"]:
    if user.id == escrower["id"]:
      if escrower["name"] != lower_name or escrower["username"] != username.lower():
        await db.update_one(
          {"client_id": client_id, "escrowers.id": escrower["id"]},
          {"$set": {"escrowers.$.name": lower_name, "escrowers.$.username": username.lower()}}
        )
      return
    is_name_clone = lower_name == escrower["name"] or lower_name.replace(' ','') == escrower["name"].replace(' ','')
    is_username_clone = username.lower() == escrower["username"]
    if is_name_clone or is_username_clone:
      await m.reply(f"""
![⚠️](tg://emoji?id=5364241851500997604) **Imposter Detected**
  **• Name:** {name}
  **• Username:** {username}
  **• Userid:** {user.id}

![⚡](tg://emoji?id=5274182275704039686) **Original escrower**
  **• Name:** {escrower["name"]}
  **• Username:** {escrower["username"]}
  **• Userid:** {escrower["id"]}
![❌](tg://emoji?id=5032973497861669622) **Looks like a scammer, please avoid him/her.**""")