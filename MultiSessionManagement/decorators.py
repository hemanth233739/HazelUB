from pyrogram import *
"""I love her. Tbh"""

def on_message(filters, group=0):
  def decorator(func):
    from . import clients
    for i in clients:
      i.on_message(filters, group=group)(func)
    return func
  return decorator