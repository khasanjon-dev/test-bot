from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from root import bot
from utils import states
from utils.callback_class import MainMenuCallback

check_test = Router()


@check_test.callback_query(MainMenuCallback.filter(F.choice == 'check_answer'))
async def check_test_menu_handler(call: CallbackQuery, state=FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(states.CheckTest.code)
    text = '🔒 Test kodini yuboring!'
    await call.message.answer(text)


@check_test.message(states.CheckTest.code)
async def get_code_handler(msg: Message, state: FSMContext):
    context = {
        'test_code': msg.text
    }
    await state.update_data(context)
    await state.set_state(states.CheckTest.answers)
    text = ("Test kalitlarini quyidagi ko'rinishda yuboring👇\n"
            "<pre>dbddabcd...</pre>\n"
            "yoki\n"
            "<pre>1d2a3b4d5a...</pre>\n\n")
    await msg.answer(text, ParseMode.HTML)


@check_test.message(states.CheckTest.answers)
async def get_answers_handler(msg: Message, state: FSMContext):
    pass
