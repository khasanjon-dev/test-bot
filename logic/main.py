from aiogram import Router, types, F
from aiogram.enums import InputMediaType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

import data
from logic.start import start_handler
from root import bot
from utils import states
from utils.callback_class import MainMenuCallback, CreateTestCallback
from utils.inlinekeyboardbuilder import inline_keyboard_builder

main = Router()


@main.message(states.MainMenu.main_menu)
async def start_menu_handler(msg: types.Message, state: FSMContext):
    strings = msg.text.split()
    if len(strings) >= 2:
        context = {
            'first_name': strings[0],
            'last_name': strings[1]
        }
        await state.update_data(context)
        await main_menu_handler(msg, state)
    else:
        await start_handler(msg, state)


@main.message(states.MainMenu.main_menu)
async def main_menu_handler(msg: types.Message, state: FSMContext):
    markup = inline_keyboard_builder(
        MainMenuCallback,
        data.main_menu.keys(),
        data.main_menu.values(),
        [1]
    )
    await msg.answer_photo(
        'https://telegra.ph/file/06c707ab1efd01a29da83.png',
        caption='Kerakli menyulardan birini tanlang',
        reply_markup=markup
    )


@main.message(states.MainMenu.create_test)
@main.callback_query(MainMenuCallback.filter(F.choice == 'create_test'))
async def create_test_menu_handler(call: CallbackQuery, state: FSMContext):
    markup = inline_keyboard_builder(
        CreateTestCallback,
        data.create_test_menu.keys(),
        data.create_test_menu.values(),
        [2, 1]
    )
    text = 'Kerakli test turini tanlang'
    await bot.edit_message_media(
        InputMediaPhoto(
            type=InputMediaType.PHOTO,
            media='https://theproductmanager.b-cdn.net/wp-content/uploads/sites/4/2021/01/PRD-Customer-Empathy-Map-Featured-Image-1280x720.png',
            caption=text
        ),
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )


@main.callback_query(CreateTestCallback.filter(F.choice == 'back'))
async def back_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(states.MainMenu.main_menu)
    await bot.delete_message(
        callback_query.message.chat.id,
        callback_query.message.message_id
    )
    await main_menu_handler(callback_query.message, state)


@main.callback_query(CreateTestCallback.filter(F.choice == 'since'))
async def since_menu_handler(call: CallbackQuery, state: FSMContext):
    pass
