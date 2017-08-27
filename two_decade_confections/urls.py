"""two_decade_confections URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from django.contrib import admin

from products.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from carts.views import CartView, CheckoutView, CheckoutFinalView
from orders.views import AddressSelectFormView, UserAddressCreateView, OrderList, OrderDetail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^products/$',
        ProductListView.as_view(), name = "products_list_view"),
    url(r'^products/(?P<pk>\d+)$',
        ProductDetailView.as_view(), name = "products_detail_view"),
    url(r'^products/(?P<slug>[\w-]+)$',
        ProductDetailView.as_view(), name = "products_slug_view"),
    url(r'^products/create/$',
        ProductCreateView.as_view(), name = "products_create_view"),
    url(r'^products/update/(?P<pk>\d+)$',
        ProductUpdateView.as_view(), name = "products_update_view"),
    url(r'^products/delete/(?P<pk>\d+)$',
        ProductDeleteView.as_view(), name = "products_delete_view"),

    url(r'^cart/$', CartView.as_view(), name = "cart"),

    url(r'^orders/$', OrderList.as_view(), name = "orders"),
    url(r'^orders/(?P<pk>\d+)$', OrderDetail.as_view(), name = "order_detail"),

    url(r'^checkout/$', CheckoutView.as_view(), name = "checkout"),
    url(r'^checkout/address/$',
        AddressSelectFormView.as_view(), name = "address_form"),
    url(r'^checkout/address/add$',
        UserAddressCreateView.as_view(), name = "user_address_create"),
    url(r'^checkout/final/$',
        CheckoutFinalView.as_view(), name = "checkout_final"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
