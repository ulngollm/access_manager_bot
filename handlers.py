import random
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery 
from services.access import Authorization
from commands.request import user as user_request
from commands.request import admin

# это фасад

def check_access(func):
    def wrapper(client, message: Message):
        if not Authorization.check_access(message.from_user.id):
            user_request.offer_ask_access(client, message)
            return
        func(client, message)
    return wrapper


# request user access
def request_access(client: Client, callback_query: CallbackQuery):
    user_request.answer(callback_query)
    admin.send_request(client, callback_query)
    

def deny_user(client: Client, callback_query: CallbackQuery):
    admin.reject_request(client, callback_query)
    user_request.notify_reject(client, callback_query)


def allow_access(client: Client, callback_query: CallbackQuery):
   admin.accept_request(client, callback_query)
   user_request.notify_success(client, callback_query)


# basic
@check_access
def reply_message(client: Client, message: Message):
    message.reply(message.text)


@check_access
def hello(client: Client, message: Message):
    message.reply(
        'Привет!'
    )


# admin
def confirm_admin_request(client: Client, message: Message):
    user_request.confirm_admin_request(client, message)


def request_admin(client: Client, callback_query: CallbackQuery):
    user_request.answer(callback_query)
    admin.request_admin(client, callback_query)


def deny_admin_access(client: Client, callback_query: CallbackQuery):
    admin.reject_admin_request(client, callback_query)
    user_request.notify_reject(client, callback_query)
    

def allow_admin_access(client: Client, callback_query: CallbackQuery):
   admin.accept_admin_request(client, callback_query)
   user_request.notify_success_admin(client, callback_query)
    