from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView

from .models import Product
# Create your views here.

class ProductListView(ListView):
    model = Product
    def get_queryset(self, *args, **kwargs):
        queryset = super(ProductListView, self).get_queryset(**kwargs)
        return queryset
class ProductDetailView(DetailView):
    model = Product
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "price",  "shipping_weight"]
    success_url = "/products/"

class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "price", "sale_price", "shipping_weight"]
    success_url = "/products/"

class ProductDeleteView(DeleteView):
    model = Product
    success_url = "/products/"
