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
from django.conf.urls import url
from django.conf.urls.static import static

from django.contrib import admin

from products import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^products/$', views.ProductListView.as_view(), name ="products_list_view"),
    url(r'^products/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name ="products_detail_view"),
    url(r'^products/(?P<slug>[\w-]+)$', views.ProductDetailView.as_view(), name ="products_slug_view"),
    url(r'^products/create/$', views.ProductCreateView.as_view(), name ="products_create_view"),
    url(r'^products/update/(?P<pk>\d+)$', views.ProductUpdateView.as_view(), name ="products_update_view"),
    url(r'^products/delete/(?P<pk>\d+)$', views.ProductDeleteView.as_view(), name ="products_delete_view"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
