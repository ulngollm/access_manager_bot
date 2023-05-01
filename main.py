from app import client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
import handlers


client.add_handler(MessageHandler(handlers.hello, filters.command(['start'])))

client.add_handler(MessageHandler(handlers.request_admin, filters.command('getadmin')))
client.add_handler(MessageHandler(handlers.reply_message, filters.text))

client.add_handler(CallbackQueryHandler(handlers.request_access, filters.regex(pattern='request:user')))
client.add_handler(CallbackQueryHandler(handlers.deny_access, filters.regex(pattern='reject:user:(\d*)')))
client.add_handler(CallbackQueryHandler(handlers.allow_access, filters.regex(pattern='accept:user:(\d*)')))

client.add_handler(CallbackQueryHandler(handlers.confirm_admin_request, filters.regex(pattern='request:admin')))
client.add_handler(CallbackQueryHandler(handlers.deny_admin_access, filters.regex(pattern='reject:admin:(\d*)')))
client.add_handler(CallbackQueryHandler(handlers.allow_admin_access, filters.regex(pattern='accept:admin:(\d*)')))


client.run()