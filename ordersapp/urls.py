from ordersapp import views
from django.urls import path

app_name = "ordersapp"

urlpatterns = [
    path('', views.OrderList.as_view(), name='orders_list'),
    path('read/<pk>/', views.OrderList.as_view(), name='orders_read'),
    path('update/<pk>/', views.OrderList.as_view(), name='orders_update'),
    path('delete/<pk>/', views.OrderList.as_view(), name='orders_delete'),
]