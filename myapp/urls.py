from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, HomeView, AdminProductListView, \
    ProductCreateView, ProductUpdateView, ReturnListView, HandleReturnView, ProductListView, PurchaseView, \
    OrderListView, ReturnView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('stuff/products/', AdminProductListView.as_view(), name='admin_product_list'),
    path('stuff/products/add/', ProductCreateView.as_view(), name='admin_add_product'),
    path('stuff/products/edit/<int:pk>/', ProductUpdateView.as_view(), name='admin_edit_product'),
    path('stuff/returns/', ReturnListView.as_view(), name='admin_return_list'),
    path('stuff/returns/<int:pk>/<str:action>/', HandleReturnView.as_view(), name='admin_handle_return'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('purchase/<int:product_id>/', PurchaseView.as_view(), name='purchase'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('return/<int:order_id>/', ReturnView.as_view(), name='return_order'),

]
