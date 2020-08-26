from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from ugc.service import get_category, get_products, get_child_category

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
    for category in categories:
        if category.children.first():
            kb.insert(InlineKeyboardButton(category.title, callback_data=category.id))
        else:
            kb.insert(InlineKeyboardButton(category.title, switch_inline_query_current_chat=category.id))
    return kb


async def child_category_kb(category_id):
    kb = InlineKeyboardMarkup(row_width=1)
    categories = await get_child_category(category_id)
    for category in categories:
        kb.insert(InlineKeyboardButton(category.title, switch_inline_query_current_chat=category.id))
    kb.add(InlineKeyboardButton('Назад◀️', callback_data='back'))
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