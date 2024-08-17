from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, ProductForm
from .models import User, Product, Return, Order
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    template_name = 'login.html'


class UserLogoutView(View):
    template_name = 'logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return LogoutView.as_view(next_page=reverse_lazy('login'))(request)


class HomeView(TemplateView):
    template_name = 'home.html'


class ProductListView(ListView):
    model = Product
    template_name = 'admin/product_list.html'
    context_object_name = 'products'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('home')
        return super().dispatch(*args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin/add_product.html'
    success_url = '/Admin/products/'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('home')
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin/edit_product.html'
    success_url = '/Admin/products/'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('home')
        return super().dispatch(*args, **kwargs)


class ReturnListView(ListView):
    model = Return
    template_name = 'admin/return_list.html'
    context_object_name = 'returns'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('home')
        return super().dispatch(*args, **kwargs)


class HandleReturnView(View):
    def get(self, request, pk, action):
        if not request.user.is_superuser:
            return redirect('home')

        return_obj = get_object_or_404(Return, pk=pk)
        order = return_obj.order
        product = order.product
        user = order.user

        if action == 'approve':
            product.stock += order.quantity
            product.save()
            user.wallet += order.quantity * product.price
            user.save()
            order.delete()
        elif action == 'reject':
            return_obj.delete()

        return redirect('Admin_return_list')
