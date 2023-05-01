
from dotenv import load_dotenv
import os
from pyrogram import Client


load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
ADMIN_LIST = os.getenv('ADMIN_LIST').split(',')

client = Client('bot', API_ID, API_HASH, bot_token=BOT_API_TOKEN)