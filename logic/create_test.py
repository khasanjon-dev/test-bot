from aiogram import Router, F
from aiogram.enums import InputMediaType, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from data import data
from logic.menu import main_menu_handler
from root import bot
from utils import states, keys_serializer
from utils.callback_class import MainMenuCallback, CreateTestCallback, CreateTestCheckCallback, BackMenuCallback
from utils.inlinekeyboardbuilder import inline_keyboard_builder
from utils.requests import create_test_request, get_or_create_user

create_test = Router()


@create_test.callback_query(MainMenuCallback.filter(F.choice == 'create_test'))
async def create_test_menu_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(states.CreateTest.menu)
    markup = inline_keyboard_builder(
        CreateTestCallback,
        data.create_test_menu.values(),
        data.create_test_menu.keys(),
        [2, 1]
    )
    text = 'Kerakli test turini tanlang'
    await bot.edit_message_media(
        InputMediaPhoto(
            type=InputMediaType.PHOTO,
            media=data.create_tes_image,
            caption=text
        ),
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )


@create_test.callback_query(BackMenuCallback.filter(F.choice == 'back_main_menu'))
async def back_main_menu_handler(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.clear()
    await state.set_state(states.MainMenu.main_menu)
    await main_menu_handler(call.message)


@create_test.callback_query(CreateTestCallback.filter(F.choice == 'back'))
async def back_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(states.MainMenu.main_menu)
    await bot.delete_message(
        callback_query.message.chat.id,
        callback_query.message.message_id
    )
    await main_menu_handler(callback_query.message)


@create_test.callback_query(CreateTestCallback.filter(F.choice == 'science'))
async def since_menu_handler(call: CallbackQuery, state: FSMContext):
    context = {
        'test_type': [
            data.create_test_menu[call.data.split(':')[1]],
            call.data.split(':')[1]
        ]
    }
    await state.update_data(context)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    text = 'Fan nomini kiriting ✍️:'
    await bot.send_message(call.message.chat.id, text)
    await state.set_state(states.CreateTest.name)


@create_test.message(states.CreateTest.name)
async def get_name_handler(msg: Message, state: FSMContext):
    context = {
        'test_name': [msg.text.capitalize(), msg.text.capitalize()]
    }
    await state.update_data(context)
    await state.set_state(states.CreateTest.keys)
    text = ("Test javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....29a30b</b>")
    await msg.answer(text, ParseMode.HTML)


@create_test.message(states.CreateTest.keys)
async def get_keys_handler(msg: Message, state: FSMContext):
    context = {
        'test_keys': [msg.text.lower(), msg.text.lower()]
    }
    await state.update_data(context)
    markup = inline_keyboard_builder(
        CreateTestCheckCallback,
        data.create_test_check.values(),
        data.create_test_check.keys(),
        [2]
    )
    get_data = await state.get_data()
    text = (f"<u>Test turi:</u>\n"
            f"<pre>{get_data['test_type'][0]}</pre>\n"
            f"<u>Fan nomi:</u>\n"
            f"<pre>{get_data['test_name'][0]}</pre>\n"
            f"<u>Testlar soni:</u>\n"
            f"<pre>{len(keys_serializer(get_data['test_keys'][0]))}</pre>\n"
            f"<u>Test kalitlari:</u>"
            f"<pre>{get_data['test_keys'][0]}</pre>\n\n"
            f"⚠️ Yuqoridagi ma'lumotlarni tasdiqlang.")
    await msg.answer(text, ParseMode.HTML, reply_markup=markup)


@create_test.callback_query(CreateTestCheckCallback.filter(F.choice == 'confirm'))
async def confirm_handler(call: CallbackQuery, state: FSMContext):
    user = await get_or_create_user(call.message.chat)
    get_data = await state.get_data()
    get_data['test_size'] = len(keys_serializer(get_data['test_keys'][0]))
    get_data['author'] = user['id']
    test = await create_test_request(get_data)
    first_text = (f"✅ Test yaratildi.\n"
                  f"Test kodi: {test['id']}\n"
                  f"Savollar soni: {test['size']}\n\n"
                  f"Quyidagi izohni o'quvchilarga yuborishingiz mumkin")
    second_text = (f"〽️ Test boshlandi.\n\n"
                   f"Test maullifi:\n"
                   f"<a href='tg://user?id={user['telegram_id']}'>{user['first_name']} {user['last_name']}</a>\n\n"
                   f"Fan: {test['name']}\n"
                   f"Savollar soni: {test['size']}\n"
                   f"Test kodi: {test['id']}\n\n"
                   f"Javoblaringizni quyidagi ko'rinishlarda yuborishingiz mumkin:\n\n"
                   f"<pre>7060#dbddabcd...\n</pre>"
                   f"yoki\n"
                   f"<pre>7060#1d2a3b4d5a...</pre>\n\n"
                   f"⚠️ Yuqoridagi ko'rinishlardan boshqa ko'rinishlarda yuborilsa tekshirish sifati buziladi!")
    markup = inline_keyboard_builder(
        BackMenuCallback,
        [data.back_buttons['back_main_menu']],
        ['back_main_menu'],
        [1]
    )
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(first_text, reply_markup=markup)
    await call.message.answer(second_text, ParseMode.HTML)
    await state.clear()
    await state.set_state(states.MainMenu.main_menu)
