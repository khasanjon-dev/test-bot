from enum import Enum

from aiogram.filters.callback_data import CallbackData


class MainMenu(str, Enum):
    create_test = 'create_test'
    check_answer = 'check_answer'
    about = 'about'
    about_me = 'about_me'


class MainMenuCallback(CallbackData, prefix='main_menu'):
    choice: MainMenu


class CreateTest(str, Enum):
    block_test = 'block_test'
    science_test = 'science_test'


class CreateTestCallback(CallbackData, prefix='test'):
    choice: CreateTest
