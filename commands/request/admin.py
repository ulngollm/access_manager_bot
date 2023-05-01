from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from services.access import Access
from services.admin import Admin


def send_request(client: Client, callback_query: CallbackQuery):
    client.send_message(
        Admin.choose_admin(),
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
    Access.allow_user(user_id)
    alert_user_acception(callback_query, user_id)


def reject_request(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    Access.deny_user(user_id)
    alert_user_rejection(callback_query, user_id)


def request_admin(client: Client, callback_query: CallbackQuery):
    client.send_message(
        Admin.choose_superadmin(),
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


def accept_admin_request(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    Admin.add_admin(user_id)
    alert_user_acception(callback_query, user_id)


def reject_admin_request(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    Admin.delete_admin(user_id)
    alert_user_rejection(callback_query, user_id)


def alert_user_acception(callback_query: CallbackQuery, user):
    callback_query.answer("Доступ для пользователя %d разрешен" % user, show_alert=True) 


def alert_user_rejection(callback_query: CallbackQuery, user):
    callback_query.answer("Доступ для пользователя %d разрешен" % user, show_alert=True) 