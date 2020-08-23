from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from ugc.service import get_category, get_products

delete = InlineKeyboardButton('❌Удалить этот товар', callback_data='delete_product')
left = InlineKeyboardButton('⬅️', callback_data='left')
right = InlineKeyboardButton('➡️', callback_data='right')
delete_cart = InlineKeyboardButton('🗑Очистить корзину', callback_data='delete_cart')

delete_confirm = InlineKeyboardMarkup(row_width=1)
delete_confirm.add(InlineKeyboardButton('Да.Точно удалить!', callback_data='yes_del'))
delete_confirm.add(InlineKeyboardButton('Отмена', callback_data='no_del'))

confirm_order = InlineKeyboardMarkup(row_width=1)
confirm_order.add(InlineKeyboardButton('Да.Заказ верен!', callback_data='confirm'))
confirm_order.add(InlineKeyboardButton('Вернуться в корзину', callback_data='back_cart'))

start_kb = ReplyKeyboardMarkup(
    row_width=1, resize_keyboard=True).add(
    KeyboardButton('Выбрать товары'), KeyboardButton('🛒Показать корзину')
)


async def category_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    categories = await get_category()
    print('category', categories)
    for category in categories:
        kb.insert(InlineKeyboardButton(category.name, switch_inline_query_current_chat=category.id))
    return kb


async def products_kb(category_id):
    kb = InlineKeyboardMarkup(row_width=1)
    items = await get_products(category_id)
    for item in items:
        kb.insert(InlineKeyboardButton(item.name, switch_inline_query_current_chat=item.id))
    kb.add(InlineKeyboardButton('Назад◀️', callback_data='back'))
    return kb


async def product_info_kb(quantity):
    kb = InlineKeyboardMarkup(row_width=2)
    quantity_btn = InlineKeyboardButton(f'{quantity} шт.', callback_data='None')
    kb.row(InlineKeyboardButton('⬇️', callback_data='down'), quantity_btn,
           InlineKeyboardButton('⬆️', callback_data='up'), InlineKeyboardButton('Отмена', callback_data='cancel'))
    kb.add(InlineKeyboardButton('🛒Добавить в корзину🛒', callback_data='add'))
    return kb


async def cart_kb(cart, cart_size, i):
    kb = InlineKeyboardMarkup(row_width=3)
    if cart_size > 1:
        kb.row(left, InlineKeyboardButton(text=f'{i + 1} / {cart_size}', callback_data='None'), right)
    kb.add(delete)
    kb.add(delete_cart)
    kb.add(InlineKeyboardButton(f'💰Оформить заказ({cart.total_price})', callback_data='pay'))
    return kb

# admin_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
#     KeyboardButton('Добавить товар'),
#     KeyboardButton('Удалить товар'),
#     KeyboardButton('Сообщить о времени доставки'),
#     KeyboardButton('Отмена'),
#     KeyboardButton('Сделать рассылку'),
#     KeyboardButton('Сделать заказ'),
#     KeyboardButton('Открыть корзину')
# )
#
# pizza_btn = InlineKeyboardButton('Шаверма', switch_inline_query_current_chat='Шаверма')
# burger_btn = InlineKeyboardButton('Закуски', switch_inline_query_current_chat='Закуски')
# snack_btn = InlineKeyboardButton('Соусы', switch_inline_query_current_chat='Соусы')
# drink_btn = InlineKeyboardButton('Напитки', switch_inline_query_current_chat='Напитки')
# position_kb = InlineKeyboardMarkup(row_width=3)
# position_kb.row(pizza_btn, burger_btn)
# position_kb.row(snack_btn, drink_btn)
#
#
# basket_kb = InlineKeyboardMarkup(row_width=1)
# basket_kb.row(pizza_btn, burger_btn)
# basket_kb.row(snack_btn, drink_btn)
# delete = InlineKeyboardButton('✖️', callback_data='del')
# left = InlineKeyboardButton('⬅️', callback_data='left')
# right = InlineKeyboardButton('➡️', callback_data='right')
# menu = InlineKeyboardButton('menu', callback_data='menu')
#
# del_kb = InlineKeyboardMarkup(row_width=1)
# del_kb.add(InlineKeyboardButton('Да, точно удалить!', callback_data='yes'))
# del_kb.add(InlineKeyboardButton('Отмена', callback_data='no'))
#
# method = InlineKeyboardMarkup(row_width=1)
# method.row(
#     InlineKeyboardButton('Доставка', callback_data='Доставка'),
#     InlineKeyboardButton('Самовывоз', callback_data='Самовывоз'),
# )
#
# time = InlineKeyboardMarkup(row_width=1)
# time.row(
#     InlineKeyboardButton('Прямо сейчас', callback_data='Прямо сейчас'),
#     InlineKeyboardButton('Ко времени', callback_data='Ко времени'),
# )
#
# pay_kb = InlineKeyboardMarkup(row_width=1)
# pay_kb.add(InlineKeyboardButton('Картой прямо сейчас', callback_data='Онлайн'),
#            InlineKeyboardButton('Наличные', callback_data='Наличные'),
#            InlineKeyboardButton('Картой курьеру', callback_data='Терминал'))
#
# confirm_kb = InlineKeyboardMarkup()
# confirm_kb.row(InlineKeyboardButton(text='Да', callback_data='yes'),
#                InlineKeyboardButton(text='Нет', callback_data='no'))
#
# delivery_time_kb = InlineKeyboardMarkup()
# delivery_time_kb.add(InlineKeyboardButton(text='Сообщить время доставки', callback_data='delivery_time'))
#
#
# def confirm(price):
#     btn = InlineKeyboardButton(f'Оформить заказ({price})', callback_data='pay')
#     return btn
#
#
# basket_kb.add(delete)
# basket_kb.add(confirm)
#
#
# def pizza_keyboard(text_btn1 = '⚪200гр', text_btn2='400гр', quantity=1):
#     pizza_kb = InlineKeyboardMarkup(row_width=1)
#     quantity_btn = InlineKeyboardButton(f'{quantity} шт.', callback_data='None')
#     pizza_kb.row(InlineKeyboardButton(text_btn1, callback_data='200'), InlineKeyboardButton(text_btn2, callback_data='400'))
#     pizza_kb.add(InlineKeyboardButton('Дополним? ', switch_inline_query_current_chat='Добавки'))
#     pizza_kb.row(InlineKeyboardButton('⬇️', callback_data='down'), quantity_btn,
#                  InlineKeyboardButton('⬆️', callback_data='up'), InlineKeyboardButton('Отмена', callback_data='cancel'))
#     pizza_kb.add(InlineKeyboardButton('Добавить в корзину', callback_data='add'))
#     return pizza_kb
#
#
# def items_keyboard(quantity = 1):
#     items_kb = InlineKeyboardMarkup(row_width=1)
#     quantity_btn = InlineKeyboardButton(f'{quantity} шт.', callback_data='None')
#     items_kb.row(InlineKeyboardButton('⬇️', callback_data='down'), quantity_btn,
#                  InlineKeyboardButton('⬆️', callback_data='up'), InlineKeyboardButton('Отмена', callback_data='cancel'))
#     items_kb.add(InlineKeyboardButton('Добавить в корзину', callback_data='add'))
#     return items_kb
#
#
# def additives_keyboard(quantity = 1):
#     items_kb = InlineKeyboardMarkup(row_width=1)
#     quantity_btn = InlineKeyboardButton(f'{quantity} шт.', callback_data='None')
#     items_kb.row(quantity_btn, InlineKeyboardButton('Отмена', callback_data='cancel'))
#     items_kb.add(InlineKeyboardButton('Дополним? ', switch_inline_query_current_chat='Добавки'))
#     items_kb.add(InlineKeyboardButton('Добавить в корзину', callback_data='add'))
#     return items_kb
#
#

#
