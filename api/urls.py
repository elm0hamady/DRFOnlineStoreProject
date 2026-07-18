from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet


urlpatterns = [
    path('products/',views.ProductListListCreateClass.as_view()),
    path('products/<int:product_id>/',views.ProductDetailsListClass.as_view()),
    path('orders/items',views.OrdersItemAPIView.as_view()),
]

router = DefaultRouter()
router.register('orders',views.OrderViewSet)
urlpatterns += router.urls
