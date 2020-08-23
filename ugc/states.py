from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    select = State()


class DeleteProduct(StatesGroup):
    delete = State()


class Checkout(StatesGroup):
    confirm = State()
    name = State()
    phone = State()