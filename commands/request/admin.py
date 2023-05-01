from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
import random
from app import ADMIN_LIST
from access import Authorization


def send_request(client: Client, callback_query: CallbackQuery):
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


def accept_request(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    Authorization.deny_access(user_id)

    callback_query.answer("Доступ для пользователя %d запрещен" % user_id, show_alert=True)


def reject_request(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    Authorization.allow_access(user_id)

    callback_query.answer("Доступ для пользователя %d разрешен" % user_id, show_alert=True)


def request_admin(client: Client, callback_query: CallbackQuery):
    client.send_message(
        # todo extract to admin service
        ADMIN_LIST[0], # только для суперпользователя
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