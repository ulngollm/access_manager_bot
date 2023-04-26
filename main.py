from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery 
import os
import random

load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
ADMIN_LIST = os.getenv('ADMIN_LIST').split(',')

app = Client('bot', API_ID, API_HASH, bot_token=BOT_API_TOKEN)
access_list = {}

class AccessStatus:
    ALLOWED = 1
    DENIED = 2


def check_access(func):
    def wrapper(client, message):
        if access_list.get(message.from_user.id) != AccessStatus.ALLOWED:
            notify_access_limit(client, message)
            return
        func(client, message)
    return wrapper


def request_access(client: Client, callback_query: CallbackQuery):
    client.send_message(
        random.choice(ADMIN_LIST),
        "Пользователь запрашивает доступ",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Просмотреть профиль",
                    user_id=callback_query.from_user.id
                )
            ],
            [
                InlineKeyboardButton(
                    "Принять",
                    callback_data= "accept:%d" % callback_query.from_user.id
                ),
                InlineKeyboardButton(
                    "Отклонить",
                    callback_data= "reject:%d" % callback_query.from_user.id
                )
            ]
        ])
    )

    callback_query.message.reply(
        "Запрос отправлен модератору. Вам придет ответ в этом чате в ближайшее время."
    )


def notify_access_limit(client: Client, message: Message):
    message.reply(
        "Привет! \nИзвините, у нас тут закрытый клуб. Если хотите запросить приглашение, нажмите на кнопку.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Пустите меня, пожалуйста",
                callback_data="request"
            )
        ]])
    )


def deny_access(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    access_list[user_id] = AccessStatus.DENIED
    callback_query.answer("Доступ для пользователя %d запрещен" % user_id, show_alert=True)
    notify_reject_user(client, user_id)


def notify_reject_user(client: Client, user_id):
    client.send_message(
        user_id,
        "Извините, ваш запрос был отклонен. Попробуйте позднее."
    )

def allow_access(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    access_list[user_id] = AccessStatus.ALLOWED
    callback_query.answer("Доступ для пользователя %d разрешен" % user_id, show_alert=True)
    notify_accept_user(client, user_id)


def notify_accept_user(client: Client, user_id):
    client.send_message(
        user_id,
        "Привет! Можешь пользоваться ботом."
    )


@check_access
def reply_message(client: Client, message: Message):
    message.reply(message.text)


@check_access
def hello(client: Client, message: Message):
    message.reply(
        'Привет!'
    )

app.add_handler(MessageHandler(hello, filters.command(['start'])))

app.add_handler(MessageHandler(reply_message, filters.text))
app.add_handler(CallbackQueryHandler(request_access, filters.regex(pattern='request')))
app.add_handler(CallbackQueryHandler(deny_access, filters.regex(pattern='reject:(\d*)')))
app.add_handler(CallbackQueryHandler(allow_access, filters.regex(pattern='accept:(\d*)')))


app.run()