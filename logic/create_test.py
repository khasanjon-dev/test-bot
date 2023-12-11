from aiogram import Router, F
from aiogram.enums import InputMediaType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from data import data
from logic.menu import main_menu_handler
from root import bot
from utils import states
from utils.callback_class import MainMenuCallback, CreateTestCallback
from utils.inlinekeyboardbuilder import inline_keyboard_builder

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


# @create_test.callback_query(BackMenuCallback.filter(F.choice =='back'))

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
        'test_type': ['Test turi: ' + data.create_test_menu[call.data.split(':')[1]], call.data.split(':')[1]]
    }
    await state.update_data(context)
    text = 'Fan nomini kiriting ✍️:'
    await bot.edit_message_caption(
        call.message.chat.id,
        call.message.message_id,
        caption=text,
    )
    await state.set_state(states.CreateTest.name)


@create_test.message(states.CreateTest.name)
async def get_name_handler(msg: Message, state: FSMContext):
    context = {
        'test_name': msg.text
    }
    await state.update_data(context)
    get_data = await state.get_data()
    text = (
        f"Test turi: {get_data['test_type']}\n"
        f"Fan nomi: {get_data['test_name']}\n\n"
        f"Test javoblarini kiriting quyidagi ko'rinishda:\n"
    )
    await bot.edit_message_caption(
        msg.chat.id,
        msg.message_id,
        caption=text
    )
