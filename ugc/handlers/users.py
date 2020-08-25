import re
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputMediaPhoto
from ugc.loader import dp, bot
from ugc.keyboards import start_kb, category_kb, product_info_kb, cart_kb, delete_confirm, confirm_order
from ugc.message_text import category_text
from ugc.service import add_new_user, get_products, get_product, add_cart, get_cart
from django.conf import settings
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from asyncio import sleep
from ugc.states import Order, DeleteProduct, Checkout


async def edit_cart(call, cart, i=0):
    cart_product = cart.get_products()
    kb = await cart_kb(cart, cart_product.count(), i)
    await call.message.edit_media(
        media=InputMediaPhoto(
            media=settings.URL + cart_product[i].product.image.url,
            caption=f'<b>{cart_product[i].product.name} {cart_product[i].product.description}.\n\n'
                    f'{cart_product[i].quantity} шт.\n\n'
                    f'{cart_product[i].product.price} руб.</b>'),
        reply_markup=kb)


async def send_cart(cart, user_id, i=0):
    cart_product = cart.get_products()
    if not cart_product:
        kb = await category_kb()
        await bot.send_message(user_id, f'Ваша корзина пуста.\n\n{category_text}',
                               reply_markup=kb)
    else:
        print('cart_product', cart_product)
        photo = settings.URL + cart_product[i].product.image.url
        kb = await cart_kb(cart, cart_product.count(), 0)
        await bot.send_photo(
            user_id,
            photo=photo,
            caption=f'<b>{cart_product[i].product.name} {cart_product[i].product.description}.\n\n'
                    f'{cart_product[i].quantity} шт.\n\n'
                    f'{cart_product[i].product.price} руб.</b>',
            reply_markup=kb
        )


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    user = await add_new_user(message)
    if user.is_admin:
        await message.answer(
            f'Привет Админ, {message.from_user.full_name}! Сделать рассылку',
            reply_markup=start_kb
        )
    else:
        await message.answer(
            f'Привет, {message.from_user.full_name}!\nДобро пожаловать в магазин ХАТА',
            reply_markup=start_kb
        )


@dp.message_handler(text='Выбрать товары', state='*')
async def choice_product(message: types.Message, state: FSMContext):
    kb = await category_kb()
    await message.answer(category_text, reply_markup=kb)


@dp.message_handler(text='🛒Показать корзину', state='*')
async def show_cart(message: types.Message, state: FSMContext):
    cart = await get_cart(message.chat.id)
    if not cart:
        await message.answer('Ваша корзина пуста.')
    else:
        await send_cart(cart, message.chat.id)
        await state.update_data(cart=cart, i=0)


@dp.inline_handler(state='*')
async def inline_categories(inline_query: InlineQuery, state: FSMContext):
    category_id = inline_query.query
    result = []
    products = await get_products(category_id)
    for product in products:
        print(settings.URL + product.image.url)
        try:
            result.append(InlineQueryResultArticle(
                id=product.id,
                thumb_url=settings.URL + product.image.url,
                title=product.name,
                description=f'{product.price} руб.',
                input_message_content=InputTextMessageContent(product.id)
            ))
        except TypeError:
            await sleep(5)
    await bot.answer_inline_query(inline_query.id, results=result, cache_time=5)
    await Order.select.set()


@dp.message_handler(state=Order.select)
async def hand_product(message: types.Message, state: FSMContext):
    quantity = 1
    product = await get_product(message.text)
    photo = settings.URL + product.image.url
    kb = await product_info_kb(quantity)
    await message.answer_photo(
        photo=photo,
        caption=f'<b>{product.description}.\n\n'
                f'{product.price} руб.</b>',
        reply_markup=kb
    )
    await state.update_data(product=product, quantity=quantity)


@dp.callback_query_handler(lambda call: call.data in ['up', 'down'], state='*')
async def up_down_handlers(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quantity = data.get('quantity')
    if call.data == 'up':
        await bot.answer_callback_query(call.id)
        quantity += 1
        kb = await product_info_kb(quantity)
        await call.message.edit_reply_markup(kb)
    if call.data == 'down':
        if quantity == 1:
            await bot.answer_callback_query(call.id, 'Невозможно выбрать меньшее количество', show_alert=False)
        else:
            await bot.answer_callback_query(call.id)
            quantity -= 1
            kb = await product_info_kb(quantity)
            await call.message.edit_reply_markup(kb)
    await state.update_data(quantity=quantity)


@dp.callback_query_handler(lambda call: call.data in ['left', 'right'], state='*')
async def left_right_handlers(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    i = data.get('i', 0)
    cart = data.get('cart')
    cart_product = cart.get_products()
    if call.data == 'right':
        await bot.answer_callback_query(call.id)
        if i != cart_product.count() - 1:
            i = i + 1
            await edit_cart(call, cart, i)
    if call.data == 'left':
        await bot.answer_callback_query(call.id)
        if i != 0:
            i = i - 1
            await edit_cart(call, cart, i)
    await state.update_data(i=i)


@dp.callback_query_handler(lambda call: call.data in ['add', 'cancel', 'delete_product', 'delete_cart', 'pay'],
                           state='*')
async def cart_handlers(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.answer_callback_query(call.id)
    if call.data == 'add':
        product = data.get('product')
        quantity = data.get('quantity')
        await add_cart(call.message.chat.id, product, quantity)
        cart = await get_cart(call.message.chat.id)
        await send_cart(cart, call.message.chat.id)
        await state.update_data(cart=cart, i=0)

    if call.data == 'cancel':
        await call.message.delete()
        kb = await category_kb()
        await call.message.answer(category_text, reply_markup=kb)

    if call.data == 'delete_cart':
        cart = data.get('cart')
        cart.delete()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer('Ваша Корзина пуста')
        kb = await category_kb()
        await call.message.answer(category_text, reply_markup=kb)

    if call.data == 'delete_product':
        await bot.answer_callback_query(call.id)
        await call.message.edit_reply_markup(reply_markup=delete_confirm)
        await DeleteProduct.delete.set()

    if call.data == 'pay':
        await bot.answer_callback_query(call.id)
        cart = data.get('cart')
        cart_product = cart.get_products()
        text = 'Ваш заказ:\n\n'
        for product in cart_product:
            text += f'{product.product.name} - {product.quantity} шт. {product.total_price} руб.\n'
        text += f'\nИтоговая стоимость заказа: {cart.total_price} руб\n'
        await call.message.answer(
            text,
            reply_markup=confirm_order
        )
        await Checkout.confirm.set()


@dp.callback_query_handler(lambda call: call.data in ['yes_del', 'no_del'], state=DeleteProduct.delete)
async def confirm_delete(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    data = await state.get_data()
    i = data.get('i')
    cart = data.get('cart')
    cart_product = cart.get_products()
    if call.data == 'yes_del':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        cart_product[i].delete()
        cart = await get_cart(call.message.chat.id)
        await send_cart(cart, call.message.chat.id, 0)
        await state.update_data(i=0, cart=cart)

    if call.data == 'no_del':
        kb = await cart_kb(cart, cart_product.count(), i)
        await call.message.edit_reply_markup(reply_markup=kb)


@dp.callback_query_handler(lambda call: call.data in ['confirm', 'back_cart'], state=Checkout.confirm)
async def confirm_handler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    data = await state.get_data()
    cart = data.get('cart')
    if call.data == 'back_cart':
        await send_cart(cart, call.message.chat.id, 0)
        await state.update_data(i=0)

    if call.data == 'confirm':
        await call.message.answer('Отлично! Введите ваше имя')
        await Checkout.name.set()


@dp.message_handler(state=Checkout.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите ваш номер телефона')
    await Checkout.phone.set()


@dp.message_handler(state=Checkout.phone)
async def phone_handler(message: types.Message, state: FSMContext):
    if re.search(r'^(8|\+?\d{1,3})?[ -]?\(?(\d{3})\)?[ -]?(\d{3})[ -]?(\d{2})[ -]?(\d{2})$', message.text):
        data = await state.get_data()
        name = data.get('name')
        cart = data.get('cart')
        cart_product = cart.get_products()
        text = 'Поступил заказ:\n\n'
        for product in cart_product:
            text += f'{product.product.name} - {product.quantity} шт. {product.total_price} руб.\n'
        text += f'\nИтоговая стоимость заказа: {cart.total_price} руб\n\n' \
                f'Покупатель:\n' \
                f'{name} - {message.text}'
        await message.answer('Ваш заказ принят. Ожидайте скоро свяжемся')
        await bot.send_message(
            int(settings.ADMIN_ID),
            text=text
        )
    else:
        await message.answer('Неправильный формат.Введите реальный номер,чтобы мы могли с вязаться с вами')
        await Checkout.phone.set()
