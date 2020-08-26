from django.urls import path

from .views import test_view, ProductDetailView


urlpatterns = [
    # path('', test_view, name='base'),
    # path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail')
]