import random
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery 
from access import Authorization
from app import ADMIN_LIST

def check_access(func):
    def wrapper(client, message: Message):
        if not Authorization.check_access(message.from_user.id):
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
                    callback_data= "accept:user:%d" % callback_query.from_user.id
                ),
                InlineKeyboardButton(
                    "Отклонить",
                    callback_data= "reject:user:%d" % callback_query.from_user.id
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
                callback_data="request:user"
            )
        ]])
    )


def deny_access(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    Authorization.deny_access(user_id)

    callback_query.answer("Доступ для пользователя %d запрещен" % user_id, show_alert=True)
    notify_reject_user(client, user_id)


def notify_reject_user(client: Client, user_id):
    client.send_message(
        user_id,
        "Извините, ваш запрос был отклонен. Попробуйте позднее."
    )

def allow_access(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    Authorization.allow_access(user_id)

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


def request_admin(client: Client, message: Message):
    message.reply(
        'Вы хотите стать админом?',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Да, отправить запрос",
                callback_data="request:admin"
            )
        ]])
    )

def confirm_admin_request(client: Client, callback_query: CallbackQuery):
    callback_query.message.reply(
        'Запрос на получение прав администратора отправлен. Ожидайте ответа в этом чате.'
    )

    client.send_message(
        # todo extract to admin service
        random.choice(ADMIN_LIST),
        "Пользователь запрашивает администраторский доступ",
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
                    callback_data= "accept:admin:%d" % callback_query.from_user.id
                ),
                InlineKeyboardButton(
                    "Отклонить",
                    callback_data= "reject:admin:%d" % callback_query.from_user.id
                )
            ]
        ])
    )

def deny_admin_access(client: Client, callback_query: CallbackQuery):
    pass


def allow_admin_access(client: Client, callback_query: CallbackQuery):
    pass