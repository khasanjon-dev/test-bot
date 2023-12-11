from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    start = State()


class MainMenu(StatesGroup):
    main_menu = State()
    create_test = State()


class CreateTest(StatesGroup):
    menu = State()
    name = State()
