from .. import *
import logging
from pyrogram import *
from pyrogram.types import *
from pyrogram import enums
import asyncio

info = logging.getLogger(__name__).info

async def is_admin(client, chat_id, user_id):
  member = await client.get_chat_member(chat_id, user_id)
  return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]

@on_message(filters.command(["unbanall", "banall", "kickall"], prefixes=HANDLER) & filters.me)
async def mass_action(app, message):
  user_id, chat_id = message.from_user.id, message.chat.id
  if not await is_admin(app, chat_id, user_id):
    return
  if message.chat.type == enums.ChatType.PRIVATE:
    return await message.reply("This Command Only works in Groups!")

  cmd = message.command[0]
  try:
    msg = await message.reply("Processing...")
    banned, count = [], 0

    if cmd == "unbanall":
      async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
        banned.append(m.user.id)
        try:
          await app.unban_chat_member(chat_id, m.user.id)
          count += 1
          await asyncio.sleep(1.2)
        except: pass
      text = f"Found Banned Members: {len(banned)}\nUnbanned Successfully: {count}"

    else:
      async for m in app.get_chat_members(chat_id):
        if not m.privileges:
          banned.append(m.user.id)
          try:
            await app.ban_chat_member(chat_id, m.user.id)
            if cmd == "kickall":
              await app.unban_chat_member(chat_id, m.user.id)
            count += 1
            await asyncio.sleep(1.2)
          except: pass
      action = "Kicked" if cmd == "kickall" else "Banned"
      text = f"Successfully {action}: {count}\nRemaining Admins: {len(banned)}"
    await message.reply(text)
    await msg.delete()
  except Exception as e:
    if "CHAT_ADMIN_REQUIRED" in str(e):
      return await message.reply("You cannot. Because you do not have enough privileges")
    await message.reply(f"**Error:** {e}")
    info(e)

MOD_NAME = 'Bans'
MOD_HELP = """**⚕️ Banall**
.banall - To ban all members from a group.
.unbanall - To unban all members from a group.
.kickall - To kick all members from a group.

**🥀 Normal-Ban**
.ban <Reply/id> - To ban them.
.kick <Reply/id> - To kick them.
.unban <Reply/id> - To unban them.
**💡 LMAO:** Don't try to test this and destroy your group!