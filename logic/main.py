from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from logic.start import start_handler
from utils import states

main = Router()


@main.message(states.MainMenu.main_menu)
async def main_menu_handler(msg: types.Message, state: FSMContext):
    strings = msg.text.split()
    if len(strings) >= 2:
        data = {
            'first_name': strings[0],
            'last_name': strings[1]
        }
        await state.update_data(data)
        await state.set_state(states.MainMenu.main_menu)
    else:
        await start_handler(msg, state)
