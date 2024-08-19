from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, ProductForm, PurchaseForm
from .models import User, Product, Return, Order
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


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


class AdminProductListView(ListView):
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
    success_url = '/stuff/products/'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('home')
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin/edit_product.html'
    success_url = '/stuff/products/'

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

        return redirect('admin_return_list')


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})


class PurchaseView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = PurchaseForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > product.stock:
                messages.error(request, 'Not enough goods in stock.')
                return redirect('product_list')

            total_price = quantity * product.price
            if total_price > request.user.wallet:
                messages.error(request, 'There are not enough funds for this purchase.')
                return redirect('product_list')

            order = Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
            )
            order.save()
            product.stock -= quantity
            product.save()
            request.user.wallet -= total_price
            request.user.save()

            messages.success(request, 'The purchase is successful!')
            return redirect('product_list')
        else:
            messages.error(request, 'Incorrect data.')
            return redirect('product_list')


class OrderListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'order_list.html', {'orders': orders})


class ReturnView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.is_clicked = True
        order.save()

        if order.user != request.user:
            return redirect('login')

        if (timezone.now() - order.created_at).total_seconds() > 180:
            messages.error(request, 'The product cannot be returned. More than 3 minutes have passed.')
            return redirect('order_list')

        Return.objects.create(order=order)
        messages.success(request, 'Return request sent.')
        return redirect('order_list')
