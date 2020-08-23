from django.contrib import admin

from .models import User, Product, Category, CartProduct, Cart


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'username')
    readonly_fields = ('user_id', 'name', 'username')


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)