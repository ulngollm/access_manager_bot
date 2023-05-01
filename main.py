from app import client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
import handlers


client.add_handler(MessageHandler(handlers.hello, filters.command(['start'])))

client.add_handler(MessageHandler(handlers.reply_message, filters.text))
client.add_handler(CallbackQueryHandler(handlers.request_access, filters.regex(pattern='request')))
client.add_handler(CallbackQueryHandler(handlers.deny_access, filters.regex(pattern='reject:(\d*)')))
client.add_handler(CallbackQueryHandler(handlers.allow_access, filters.regex(pattern='accept:(\d*)')))


client.run()