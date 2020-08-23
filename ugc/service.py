from ugc.models import User, Category, Product, Cart, CartProduct
from asgiref.sync import sync_to_async


@sync_to_async
def add_new_user(message):
    user, created = User.objects.get_or_create(
        user_id=message.chat.id,
        defaults={
            'name': message.from_user.full_name,
            'username': message.from_user.username
        }
    )
    return user


@sync_to_async
def get_category():
    return Category.objects.all()


@sync_to_async
def get_products(category_id):
    print(category_id)
    #return Items.objects.all().filter(category__icontains=category)
    return Product.objects.all()


@sync_to_async
def get_product(pk):
    return Product.objects.get(pk=pk)


@sync_to_async
def add_cart(user_id, product, quantity):
    user = User.objects.get(user_id=user_id)
    cart, _ = Cart.objects.get_or_create(user=user)
    print(cart)
    cart_product, _ = CartProduct.objects.get_or_create(user=user, cart=cart, product=product, quantity=quantity)
    print('created', _)
    if _:
        cart.product.add(cart_product)


@sync_to_async
def get_cart(user_id):
    cart = Cart.objects.get(user__user_id=user_id)
    return cart