from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,OrderCreateSerializer
from api.models import Product,Order,OrderItem
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers,vary_on_cookie
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter ,InStockFilterBackend ,OrderFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination




class ProductListClass(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    

class ProductListListCreateClass(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        InStockFilterBackend,
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    # pagination_class = LimitOffsetPagination
    pagination_class = None
    # pagination_class.page_size = 3
    # pagination_class.max_page_size = 4
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.page_query_param = 'pagenum'

    search_fields = ['name','description']
    ordering_fields = ['name','stock','price']
    
    @method_decorator(cache_page(60*15,key_prefix='product_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    

class ProductDetailsListClass(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['POST','PUT','PATCH']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# class OrderListClass(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    @method_decorator(cache_page(60 * 15, key_prefix='product_list'))
    @method_decorator(vary_on_headers('Authorization'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    # @action(detail=False,methods=['get'],url_path='user-orders',permission_classes=[IsAuthenticated])
    # def user_orders(self,request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders,many=True)
    #     return Response(serializer.data)
    

class UserOrderListClass(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     seializer = ProductSerializer(products,many=True)
#     return Response(seializer.data)

# @api_view(['GET'])
# def product_detail(request,pk):
#     product = get_object_or_404(Product,pk=pk)
#     seializer = ProductSerializer(product)
#     return Response(seializer.data)

# @api_view(['GET'])
# def orders_list(request):
#     orders = Order.objects.prefetch_related('items__product')
#     seializer = OrderSerializer(orders,many=True)
#     return Response(seializer.data)

# @api_view(['GET'])
# def orders_item(request):
#     order_items = OrderItem.objects.all()
#     seializer = OrderItemSerializer(order_items,many=True)
#     return Response(seializer.data)

class OrdersItemAPIView(APIView):
    def get(self,request):
        order_items = OrderItem.objects.all()
        seializer = OrderItemSerializer(order_items,many=True)
        return Response(seializer.data)
