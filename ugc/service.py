from ugc.models import UserBot, Category, Product, Cart, CartProduct
from asgiref.sync import sync_to_async


@sync_to_async
def add_new_user(message):
    user, created = UserBot.objects.get_or_create(
        user_id=message.chat.id,
        defaults={
            'name': message.from_user.full_name,
            'username': message.from_user.username
        }
    )
    return user


@sync_to_async
def get_category():
    return Category.objects.filter(parent=None)


@sync_to_async
def get_child_category(category_id):
    return Category.objects.filter(parent__id=category_id)


@sync_to_async
def get_products(category_id):
    return Product.objects.all().filter(category__id=category_id)


@sync_to_async
def get_product(pk):
    return Product.objects.get(pk=pk)


@sync_to_async
def add_cart(user_id, product, quantity):
    user = UserBot.objects.get(user_id=user_id)
    cart = Cart.objects.filter(user=user).first()
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
    return Cart.objects.filter(user__user_id=user_id).first()


@sync_to_async
def make_order(user_id, name, phone):
    return Cart.objects.filter(user__user_id=user_id).first()