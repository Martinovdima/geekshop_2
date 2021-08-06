from ordersapp import views
from django.urls import path

app_name = "ordersapp"

urlpatterns = [
    path('', views.OrderList.as_view(), name='order_list'),
    path('create/', views.OrderItemCreate.as_view(), name='order_create'),
    path('read/<pk>/', views.OrderItemsRead.as_view(), name='order_read'),
    path('update/<pk>/', views.OrderItemUpdate.as_view(), name='order_update'),
    path('delete/<pk>/', views.OrderItemsDelete.as_view(), name='order_delete'),
    path('forming/complete/<pk>/', views.order_forming_complete, name='order_forming_complete'),
]