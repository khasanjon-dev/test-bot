from aiogram import Router, F
from aiogram.enums import InputMediaType, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from data import data
from logic.menu import main_menu_handler
from root import bot
from utils import states, keys_serializer
from utils.callback_class import MainMenuCallback, CreateTestCallback, CreateTestCheckCallback
from utils.inlinekeyboardbuilder import inline_keyboard_builder
from utils.requests import create_test_request

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
        'test_type': [f"<u>Test turi:</u> \n<pre>{data.create_test_menu[call.data.split(':')[1]]}</pre>",
                      call.data.split(':')[1]]
    }
    await state.update_data(context)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    text = 'Fan nomini kiriting ✍️:'
    await bot.send_message(call.message.chat.id, text)
    await state.set_state(states.CreateTest.name)


@create_test.message(states.CreateTest.name)
async def get_name_handler(msg: Message, state: FSMContext):
    context = {
        'test_name': [f'<u>Fan nomi:</u> <pre><b>\n{msg.text.capitalize()}</b></pre>', msg.text.capitalize()]
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
        'test_keys': [f'<u>Test kalitlari:</u> \n<pre>{msg.text.lower()}</pre>', msg.text.lower()]
    }
    await state.update_data(context)
    markup = inline_keyboard_builder(
        CreateTestCheckCallback,
        data.create_test_check.values(),
        data.create_test_check.keys(),
        [2]
    )
    get_data = await state.get_data()
    text = (f"{get_data['test_type'][0]}\n"
            f"{get_data['test_name'][0]}\n"
            f"<u>Testlar soni:</u> <pre>{30}</pre>"
            f"{get_data['test_keys'][0]}\n")
    await msg.answer(text, ParseMode.HTML, reply_markup=markup)


@create_test.callback_query(CreateTestCheckCallback.filter(F.choice == 'confirm'))
async def confirm_handler(call: CallbackQuery, state: FSMContext):
    get_data = await state.get_data()
    get_data['test_size'] = len(keys_serializer(get_data['test_keys'][0]))
    get_data['author'] = call.mess
    await create_test_request(get_data)
