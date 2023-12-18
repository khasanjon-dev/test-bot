"""This package is used for a bot logic implementation."""
from .check_test import check_test
from .create_test import create_test
from .menu import menu
from .start import start

routers = (start, menu, create_test, check_test)
