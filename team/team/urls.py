"""
URL configuration for team project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    
"""
from django.contrib import admin
from django.urls import path
from . import home
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.landing_page,  name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('order-detail/<int:id>/<str:productName>', home.order_detail, name='order-detail'),
    path('preview-orders', home.previewOrders, name='preview-orders'),
    path('shipping', home.shipping, name='shipping'),
    path('checkout', home.pay, name='checkout'),
    path('subscribe', home.subscribe, name='subscribe'),
    path('edit-customer', views.editCustomer, name='edit-customer'),
    path('success', home.success, name='success'),
    path('pay_success', home.pay_success, name='pay_success'),
    path('confirm/<str:id>', views.confirm, name='confirm')
]
