from django.contrib import admin

from .models import CustomerBot, CustomerSite, Product, Category, CartProduct, Cart, Order


@admin.register(CustomerBot)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'username')
    readonly_fields = ('user_id', 'name', 'username')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_select_related = ('parent',)
    list_display = ('title', 'parent', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['parent']
        else:
            return []


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(CustomerSite)