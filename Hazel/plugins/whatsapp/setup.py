from Hazel import *
from pyrogram import *
from pywa import WhatsApp
import qrcode
import logging

wa_info = {
  "connected": False,
  "qr_path": "",
  "client": WhatsApp(session="HazelWhatsapp")
}
wa=wa_info['client']
async def start_wa():
  """
  wa_client = wa_info['client']
  qrstr = await wa_client.get_qr_code()
  qr=qrcode.make(qrstr)
  qr.save('ub/wa_qr.png')
  wa_info["qr_path"] = 'ub/wa_qr.png'
  await wa_client.start()
  logging.info("Whatsapp qr created! use .walogin to get qr.")"""

@app.on_message(filters.command('walogin', prefixes=HANDLER))
async def walogin(_,m):
  if ('qr_path' in wa_info):
    await m.reply_photo(wa_info['qr_path'])

#@wa.on_ready()
async def wa_onready():
  await app.send_message('me', "Whatsapp linked successfully!")
  logging.info("Whatsapp client logged-in.")