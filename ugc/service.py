import aiohttp
from ugc.models import CustomerBot, Category, Product, Cart, CartProduct, Order
from asgiref.sync import sync_to_async
from django.conf import settings
from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category']


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['parent', 'children']

@sync_to_async
def add_new_user(message):
    user, created = CustomerBot.objects.get_or_create(
        user_id=message.chat.id,
        defaults={
            'name': message.from_user.full_name,
            'username': message.from_user.username
        }
    )
    return user


# @sync_to_async
# def get_category():
#     return Category.objects.filter(parent=None)


# @sync_to_async
# def get_child_category(category_id):
#     return Category.objects.filter(parent__id=category_id)


# @sync_to_async
# def get_products(category_id):
#     return Product.objects.all().filter(category__id=category_id)


@sync_to_async
def get_product(pk):
    return Product.objects.get(pk=pk)


@sync_to_async
def add_cart(user_id, product, quantity):
    user = CustomerBot.objects.get(user_id=user_id)
    cart = Cart.objects.filter(user=user, in_order=False).first()
    if not cart:
        cart = Cart.objects.create(user=user)
    cart_product, created = CartProduct.objects.get_or_create(user=user, cart=cart, product=product)
    if not created:
        cart_product.quantity = quantity + cart_product.quantity
    else:
        cart_product.quantity = quantity
    cart_product.save()
    cart.save()


@sync_to_async
def get_cart(user_id):
    return Cart.objects.filter(user__user_id=user_id, in_order=False).first()


@sync_to_async
def make_order(user_id, cart, name, phone):
    customer_bot = CustomerBot.objects.get(user_id=user_id)
    print('cart', cart)
    print('type cart', type(cart))
    Order.object.create(customer_bot=customer_bot, name=name, phone=phone, cart=cart)


async def get_products(category_id):
    url = settings.URL + '/api' + '/products'
    async with aiohttp.ClientSession() as session:
        params = {'category': category_id}
        response = await session.get(url, params=params)
        data = await response.json()
        print('data', data)
        return data


async def get_category():
    url = settings.URL + '/api' + '/category'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json()
        print('category', data)
        return data


async def get_child_category(category_id):
    url = settings.URL + '/api' + '/category'
    async with aiohttp.ClientSession() as session:
        params = {'parent': category_id}
        response = await session.get(url, params=params)
        data = await response.json()
        print('data', data)
        return data
