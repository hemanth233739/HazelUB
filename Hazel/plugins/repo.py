from .. import *
from pyrogram import *
from pyrogram.types import LinkPreviewOptions

@on_message(filters.command("repo", prefixes=HANDLER) & filters.user('me'))
async def repo(_, message):
  if message.reply_to_message:
    return await message.reply_to_message.reply("https://github.com/DevsBase/HazelUB", link_preview_options=LinkPreviewOptions(is_disabled=True))
  await message.reply("https://github.com/DevsBase/HazelUB", link_preview_options=LinkPreviewOptions(is_disabled=True))