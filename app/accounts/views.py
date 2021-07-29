from django.shortcuts import render, redirect
from .utils.account import is_user_authorized_to_visit_page
from accounts.utils.customer.account import CustomerSettings
from .utils.product import SaveNewProduct, ProductDeleter
from .utils.order import OrderDeleter
from accounts.utils.admin.order import OrderUpdate, OrdersListAdmin
from accounts.utils.admin.product import ProductListAdmin
from accounts.utils.customer.order import NewOrderCustomer, OrdersListCustomer
from accounts.utils.customer.product import ProductListCustomer
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import unauthenticated_user, allowed_user
from django.views import View


def redirect_groups(request, if_admin, if_customer):
    group = request.user.groups.all()[0].name
    if group == 'admin':
        return redirect(if_admin)
    elif group == 'customer':
        return redirect(if_customer)


@login_required(login_url='login')
def redirectHome(request):
    return redirect_groups(request, if_admin='admin_page', if_customer='customer_page')


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
    if request.method == 'POST':
        CustomerSettings(request).save_settings()
        messages.success(request, 'Account Settings Saved')
    customer = request.user.customer
    form_initial = {'name':customer.name,
                    'phone':customer.phone,
                    'email': customer.user.email}
    info_form = CustomerForm(data=form_initial, instance=customer)
    profile_pic_form = ProfilePictureForm()
    context = {'info_form': info_form,
               'profile_pic_form': profile_pic_form}

    return render(request, 'accounts/accounts_settings.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def home(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders,
               'total_orders': total_orders,
                'delivered': delivered,
                'pending': pending}
    return render(request, 'accounts/user.html', context)


class LoginPage(View):
    @method_decorator(unauthenticated_user)
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is Incorrect')

    @method_decorator(unauthenticated_user)
    def get(self, request):
        context = {}
        return render(request, 'accounts/login.html', context)


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('login')


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Account Was Created for {form.cleaned_data.get("username")}')

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def adminPage(request):
    orders = Order.objects.order_by('date_created')
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders[:5],
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'customer'])
def products(request):
    return redirect_groups(request, if_admin='admin_products', if_customer='customer_products')


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def adminProducts(request):
    products = ProductListAdmin().get_product_list()
    context = {'products': products,
               'show_availability': True}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def customerProducts(request):
    products = ProductListCustomer().get_product_list()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def editProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        SaveNewProduct(request, edit_instance=product).create_new_product()
        messages.success(request, 'Product Successfully Edited')
        return redirect('edit_product', pk=pk)
    tags = ', '.join([t.name for t in product.tags.all()])
    edit_form = NewProductForm(initial={'tags': tags},
                               instance=product)
    context = {'product_pic': product.product_pic,
               'edit_form': edit_form}
    return render(request, 'accounts/product_edit.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def newProduct(request):
    if request.method == 'POST':
        SaveNewProduct(request).create_new_product()
        messages.success(request, 'New Product Successfully Saved')
        return redirect('new_product')
    prodForm = NewProductForm()
    context = {'prodForm': prodForm}
    return render(request, 'accounts/new_product.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteProduct(request, pk):
    if request.method == 'POST':
        ProductDeleter(pk).delete_product()
        messages.success(request, 'Product Successfully Deleted')
        return redirect('products')
    product = Product.objects.get(id=pk)
    related_orders = Order.objects.filter(product__id=pk)
    context = {'related_orders': related_orders,
               'product_name': product.name,
               'orders': related_orders,
               'product_pic': product.product_pic}
    return render(request, 'accounts/product_delete.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'customer'])
def customer(request, customer_id, page):
    authorized = is_user_authorized_to_visit_page(request.user, customer_id)
    if not authorized:
        return redirect('/')

    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()
    orders_count = orders.count()

    page = int(page)
    lister = OrdersListCustomer(request, page, customer_id)
    orders = lister.get_orders()
    filter_form = OrderFilterForm(initial=request.GET)

    context = {'customer': customer,
               'orders': orders,
               'orders_count': orders_count,
               'filter_form': filter_form,
               'next_page': page + 1,
               'prev_page': page - 1,
               'pages_count': lister.count_pages(),
               }

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def createOrder(request, pk):
    if request.method == 'POST':
        NewOrderCustomer(request, pk).save_order()
        messages.success(request, 'Order Successfully Saved.')
        return redirect('products')

    product = Product.objects.get(id=pk)
    context = {'product_name': product.name,
               'product_pic': product.product_pic,
               'product_price': product.price,
               'new_order_form': NewOrderForm(initial={'quantity': 1})}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = UpdateOrderForm(instance=order)
    if request.method == 'POST':
        OrderUpdate(request, order).update_order()
        messages.success(request, 'Order Successfully Updated')
        return redirect('admin_page')

    context = {'product': order.product,
               'update_form': form,
               'order_quantity': order.quantity}
    return render(request, 'accounts/order_update.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    authorized = is_user_authorized_to_visit_page(request.user, order.customer.id)
    if not authorized:
        messages.error(request, "You're Not Authorized to Change This Order")
        return redirect('customer', customer_id=request.user.id)

    if request.method == 'POST':
        deleter = OrderDeleter(order)
        deleter.delete_order()
        status = deleter.get_delete_status()
        if status['status'] == 'success':
            messages.success(request, status['msg'])
            return redirect('customer', customer_id=request.user.id)
        else:
            messages.error(request, status['msg'])
            return redirect('customer', customer_id=request.user.id)

    context = {'item': order}
    return render(request, 'accounts/delete_order.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def showOrders(request, page):
    page = int(page)
    lister = OrdersListAdmin(request, page)
    orders = lister.get_orders()
    filter_form = OrderFilterForm(initial=request.GET)
    context = {'orders': orders,
               'page': page,
               'next_page': page+1,
               'prev_page': page-1,
               'pages_count': lister.count_pages(),
               'filter_form': filter_form}
    return render(request, 'accounts/order_all.html', context)
