from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet


class CategoryView(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     query = self.request.data.get("query")
    #     print('query: ', query)
    #     print('queryset', self)