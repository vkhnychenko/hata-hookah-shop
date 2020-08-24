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
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        cart = Cart.objects.create(user=user)
    print('cart', cart)
    cart_product, created = CartProduct.objects.get_or_create(user=user, cart=cart, product=product)
    if not created:
        cart_product.quantity = quantity + cart_product.quantity
    else:
        cart_product.quantity = quantity
    cart_product.save()
    print('cart_product', cart_product)
    print('created', created)
    # print('product_create', cart_product_create)
    cart.save()
    # if cart_product_create:
    #     print(cart_product_create)
        # cart.product.add(cart_product)


@sync_to_async
def get_cart(user_id):
    cart = Cart.objects.filter(user__user_id=user_id).first()
    print('cart', cart)
    return cart