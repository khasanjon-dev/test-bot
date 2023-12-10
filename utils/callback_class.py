from enum import Enum

from aiogram.filters.callback_data import CallbackData


class BackMenu(str, Enum):
    back = 'back'
    back_main_menu = 'back_main_menu'


class BackMenuCallback(CallbackData, prefix='back'):
    back: BackMenu
    back_main_menu: BackMenu


class MainMenu(str, Enum):
    create_test = 'create_test'
    check_answer = 'check_answer'
    about = 'about'
    about_me = 'about_me'


class MainMenuCallback(CallbackData, prefix='main_menu'):
    choice: MainMenu


class CreateTest(str, Enum):
    block_test = 'block'
    science_test = 'science'
    back = 'back'


class CreateTestCallback(CallbackData, prefix='test'):
    choice: CreateTest
