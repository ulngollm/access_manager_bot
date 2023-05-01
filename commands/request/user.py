from pyrogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client


def offer_ask_access(client: Client, message: Message):
    message.reply(
        "Привет! \nИзвините, у нас тут закрытый клуб. Если хотите запросить приглашение, нажмите на кнопку.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Пустите меня, пожалуйста",
                callback_data="request:user"
            )
        ]])
    )

def confirm_admin_request(client: Client, message: Message):
    message.reply(
        'Вы хотите стать админом?',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Да, отправить запрос",
                callback_data="request:admin"
            )
        ]])
    )

def answer(callback_query: CallbackQuery):
    callback_query.message.reply(
        "Запрос отправлен модератору. Вам придет ответ в этом чате в ближайшее время."
        )


def notify_reject(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    
    client.send_message(
        user_id,
        "Извините, ваш запрос был отклонен. Попробуйте позднее."
    )


def notify_success(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    
    client.send_message(
        user_id,
        "Привет! Можешь пользоваться ботом."
    )

def notify_success_admin(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    
    client.send_message(
        user_id,
        "Теперь у вас есть права администратора. Вы можете принимать заявки от пользователей на получение доступа."
    )