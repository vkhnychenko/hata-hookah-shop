from time import timezone

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# class Customer(models.Model):
#
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
#     address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
#     orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')
#
#     def __str__(self):
#         return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class UserBot(models.Model):
    user_id = models.PositiveIntegerField(verbose_name='ID пользователя', unique=True)
    name = models.CharField(verbose_name='Имя пользователя', max_length=50)
    username = models.CharField(verbose_name='Никнейм пользователя', max_length=50)
    is_admin = models.BooleanField(verbose_name='Админ', default=False)

    def __str__(self):
        return f'{self.user_id} {self.name} {self.username} {self.is_admin}'

    class Meta:
        verbose_name = 'Профиль пользователя бота'
        verbose_name_plural = 'Профили пользователей бота'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=50)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField('Наименование товара', max_length=50)
    description = models.CharField(max_length=50, blank=True)
    image = models.ImageField('Картинка товара', upload_to='items/')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CartProduct(models.Model):
    user = models.ForeignKey(UserBot, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'Объект корзины'
        verbose_name_plural = 'Объекты корзины'


class Cart(models.Model):
    user = models.ForeignKey(UserBot, verbose_name='Владелец', on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена товаров в корзине',
                                      default=0)

    def get_products(self):
        products = self.related_products.all()
        return products

    def save(self, *args, **kwargs):
        products = self.related_products.all()
        cart_total_price = 0
        for product in products:
            cart_total_price += product.total_price
        self.total_price = cart_total_price
        self.total_products = products.count()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.user_id}'

    class Meta:
        verbose_name = 'Корзина товаров'
        verbose_name_plural = 'Корзина товаров'


# class Order(models.Model):
#
#     STATUS_NEW = 'new'
#     STATUS_IN_PROGRESS = 'in_progress'
#     STATUS_READY = 'is_ready'
#     STATUS_COMPLETED = 'completed'
#
#     BUYING_TYPE_SELF = 'self'
#     BUYING_TYPE_DELIVERY = 'delivery'
#
#     STATUS_CHOICES = (
#         (STATUS_NEW, 'Новый заказ'),
#         (STATUS_IN_PROGRESS, 'Заказ в обработке'),
#         (STATUS_READY, 'Заказ готов'),
#         (STATUS_COMPLETED, 'Заказ выполнен')
#     )
#
#     BUYING_TYPE_CHOICES = (
#         (BUYING_TYPE_SELF, 'Самовывоз'),
#         (BUYING_TYPE_DELIVERY, 'Доставка')
#     )
#
#     user = models.ForeignKey(UserBot, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255, verbose_name='Имя')
#     phone = models.CharField(max_length=20, verbose_name='Телефон')
#     cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
#     address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
#     status = models.CharField(
#         max_length=100,
#         verbose_name='Статус заказ',
#         choices=STATUS_CHOICES,
#         default=STATUS_NEW
#     )
#     buying_type = models.CharField(
#         max_length=100,
#         verbose_name='Тип заказа',
#         choices=BUYING_TYPE_CHOICES,
#         default=BUYING_TYPE_SELF
#     )
#     comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
#     order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)
#
#     def __str__(self):
#         return str(self.id)