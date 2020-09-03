from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Category, Product


class ProductSerializer(ModelSerializer):
    # products = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = ("id", "title", "description", "image", "price", "category")


class CategorySerializer(ModelSerializer):
    product_set = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "title", "parent", "product_set", "children")