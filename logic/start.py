from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from logic.menu import main_menu_handler
from utils import states

start = Router()


@start.message(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    await state.set_state(states.MainMenu.main_menu)
    await main_menu_handler(msg)
    # text = ("Hurmatli foydalanuvchi ism familiyangizni quyidagi ko'rinishda kiriting 👇👇👇\n"
    #         "Ism Familiya\n\n"
    #         "Misol:\n"
    #         "Akbar Avazov")
    # await msg.answer(text)
