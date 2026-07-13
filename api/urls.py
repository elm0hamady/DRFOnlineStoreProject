from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('products/',views.ProductListListCreateClass.as_view()),
    path('products/<int:product_id>/',views.ProductDetailsListClass.as_view()),
    path('orders/',views.OrderListClass.as_view()),
    path('orders/items',views.OrdersItemAPIView.as_view()),
    path('user-orders/', views.UserOrderListClass.as_view(), name='user-orders'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
