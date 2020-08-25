from django.contrib import admin

from .models import UserBot, Product, Category, CartProductBot, CartBot


@admin.register(UserBot)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'username')
    readonly_fields = ('user_id', 'name', 'username')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_select_related = ('parent',)
    list_display = ('title', 'parent', )


admin.site.register(Product)
admin.site.register(CartBot)
admin.site.register(CartProductBot)