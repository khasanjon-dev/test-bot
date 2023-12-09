from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import data
from logic.start import start_handler
from root import bot
from utils import states
from utils.callback_class import MainMenuCallback, CreateTestCallback
from utils.inlinekeyboardbuilder import inline_keyboard_builder

main = Router()


@main.message(states.MainMenu.main_menu)
async def main_menu_handler(msg: types.Message, state: FSMContext):
    strings = msg.text.split()
    if len(strings) >= 2:
        markup = inline_keyboard_builder(
            MainMenuCallback,
            data.main_menu.keys(),
            data.main_menu.values(),
            [1]
        )
        context = {
            'first_name': strings[0],
            'last_name': strings[1]
        }
        await state.update_data(context)
        await msg.answer_photo('https://telegra.ph/file/06c707ab1efd01a29da83.png', caption='Asosiy menyu',
                               reply_markup=markup)
        # await msg.answer(f"Asosiy menyu", reply_markup=markup)
    else:
        await start_handler(msg, state)


@main.message(states.MainMenu.create_test)
@main.callback_query(MainMenuCallback.filter(F.choice == 'create_test'))
async def create_test_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    markup = inline_keyboard_builder(
        CreateTestCallback,
        data.create_test_menu.keys(),
        data.create_test_menu.values(),
        [1]
    )
    text = 'Kerakli test turini tanlang'
    await bot.edit_message_text(
        text,
        callback_query.message.chat.id,
        callback_query.message.message_id,
        reply_markup=markup
    )
