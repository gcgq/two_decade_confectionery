from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings

from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView

from .models import Product
from two_decade_confections.mixins import SlugMixin
# Create your views here.

class ProductListView(ListView):
    model = Product
    def get_queryset(self, *args, **kwargs):
        queryset = super(ProductListView, self).get_queryset(**kwargs)
        return queryset
class ProductDetailView(SlugMixin, DetailView):
    model = Product
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "category", "price",  "weight"]
    success_url = "/products/"

class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "category", "price", "sale_price", "weight","active"]
    success_url = "/products/"

class ProductDeleteView(DeleteView):
    model = Product
    success_url = "/products/"
