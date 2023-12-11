from aiogram import Router, types

import data
from utils import states
from utils.callback_class import MainMenuCallback
from utils.inlinekeyboardbuilder import inline_keyboard_builder

menu = Router()


# @menu.message(states.MainMenu.main_menu)
# async def start_menu_handler(msg: types.Message, state: FSMContext):
#     strings = msg.text.split()
#     if len(strings) >= 2:
#         context = {
#             'first_name': strings[0],
#             'last_name': strings[1]
#         }
#         await state.update_data(context)
#         await main_menu_handler(msg)
#     else:
#         await start_handler(msg, state)


@menu.message(states.MainMenu.main_menu)
async def main_menu_handler(msg: types.Message):
    markup = inline_keyboard_builder(
        MainMenuCallback,
        data.main_menu.values(),
        data.main_menu.keys(),
        [1]
    )
    await msg.answer_photo(
        'https://telegra.ph/file/06c707ab1efd01a29da83.png',
        caption='Kerakli menyulardan birini tanlang',
        reply_markup=markup
    )
