from django.urls import path
from . import views



urlpatterns = [
    path('products/',views.ProductListListCreateClass.as_view()),
    path('products/<int:product_id>/',views.ProductDetailsListClass.as_view()),
    path('orders/',views.OrderListClass.as_view()),
    path('orders/items',views.OrdersItemAPIView.as_view()),
    path('user-orders/', views.UserOrderListClass.as_view(), name='user-orders'),
]
