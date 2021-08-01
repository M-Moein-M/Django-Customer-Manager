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


class RedirectHome(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        group = request.user.groups.all()[0].name
        if group == 'admin':
            return redirect('admin_page')
        elif group == 'customer':
            return redirect('customer_page')


class AccountSettings(View):
    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['customer'])])
    def get(self, request):
        customer = request.user.customer
        form_initial = {'name': customer.name,
                        'phone': customer.phone,
                        'email': customer.user.email}
        info_form = CustomerForm(data=form_initial, instance=customer)
        profile_pic_form = ProfilePictureForm()
        context = {'info_form': info_form,
                   'profile_pic_form': profile_pic_form}

        return render(request, 'accounts/accounts_settings.html', context)

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['customer'])])
    def post(self, request):
        CustomerSettings(request).save_settings()
        messages.success(request, 'Account Settings Saved')
        return self.get(request)


@method_decorator([login_required(login_url='login'),
                   allowed_user(allowed_roles=['customer'])], name='get')
class Home(View):
    def get(self, request):
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


class RegisterPage(View):
    form_class = CreateUserForm

    @method_decorator(unauthenticated_user)
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            msg = f'Account Was Created for {form.cleaned_data.get("username")}'
            messages.success(request, msg)
            return redirect('login')

    @method_decorator(unauthenticated_user)
    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)


@method_decorator([login_required(login_url='login'),
                   allowed_user(allowed_roles=['admin'])], name='get')
class AdminPage(View):
    def get(self, request):
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


class NewPack(View):
    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def get(self, request):
        context = {'packForm': NewPackForm()}
        return render(request, 'accounts/new_pack.html', context)

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def post(self, request):
        # SaveNewPack(request).create_new_pack()
        SaveNewProduct(request, form_class=NewPackForm).create_new_product()
        messages.success(request, 'New Pack Successfully Saved')
        return redirect('new_pack')


class EditPack(View):
    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def get(self, request, pk):
        pack = Pack.objects.get(id=pk)
        tags = ', '.join([t.name for t in pack.tags.all()])
        edit_form = NewPackForm(initial={'tags': tags},
                                instance=pack)
        context = {'product_pic': pack.product_pic,
                   'edit_form': edit_form}
        return render(request, 'accounts/pack_edit.html', context)

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def post(self, request, pk):
        pack = Pack.objects.get(id=pk)
        SaveNewProduct(request,
                       edit_instance=pack,
                       form_class=NewPackForm).create_new_product()
        messages.success(request, 'Pack Successfully Edited')
        return redirect('edit_pack', pk=pk)


@method_decorator([login_required(login_url='login'),
                   allowed_user(allowed_roles=['admin', 'customer'])],
                  name='get')
class Products(View):
    def get(self, request):
        group = request.user.groups.all()[0].name
        if group == 'admin':
            return self.render_admin_products(request)
        elif group == 'customer':
            return self.render_customer_products(request)

    def render_admin_products(self, request):
        products = ProductListAdmin().get_product_list()
        context = {'products': products,
                   'show_availability': True}
        return render(request, 'accounts/products.html', context)

    def render_customer_products(self, request):
        products = ProductListCustomer().get_product_list()
        return render(request, 'accounts/products.html', {'products': products})


class EditProduct(View):
    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def get(self, request, pk):
        if self.is_subclass_instance(pk):
            return redirect('edit_pack', pk=pk)

        product = Product.objects.get(id=pk)
        tags = ', '.join([t.name for t in product.tags.all()])
        edit_form = NewProductForm(initial={'tags': tags},
                                   instance=product)
        context = {'product_pic': product.product_pic,
                   'edit_form': edit_form}
        return render(request, 'accounts/product_edit.html', context)

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def post(self, request, pk):
        if self.is_subclass_instance(pk):
            messages.error(request, 'Edit Was Not Saved! Try Again')
            return redirect('edit_pack', pk=pk)

        product = Product.objects.get(id=pk)
        SaveNewProduct(request, edit_instance=product).create_new_product()
        messages.success(request, 'Product Successfully Edited')
        return redirect('edit_product', pk=pk)

    def is_subclass_instance(self, pk):
        return Pack.objects.filter(id=pk).exists()


class NewProduct(View):
    form_class = NewProductForm

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def post(self, request):
        SaveNewProduct(request).create_new_product()
        messages.success(request, 'New Product Successfully Saved')
        return redirect('new_product')

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def get(self, request):
        prodForm = self.form_class()
        context = {'prodForm': prodForm}
        return render(request, 'accounts/new_product.html', context)


class DeleteProduct(View):
    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def post(self, request, pk):
        ProductDeleter(pk).delete_product()
        messages.success(request, 'Product Successfully Deleted')
        return redirect('products')

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        related_orders = Order.objects.filter(product__id=pk)
        context = {'related_orders': related_orders,
                   'product_name': product.name,
                   'orders': related_orders,
                   'product_pic': product.product_pic}
        return render(request, 'accounts/product_delete.html', context)


class CustomerOrders(View):
    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin', 'customer'])])
    def get(self, request, customer_id, page):
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


class CreateOrder(View):
    form_class = NewOrderForm

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['customer'])])
    def post(self, request, pk):
        NewOrderCustomer(request, pk).save_order()
        messages.success(request, 'Order Successfully Saved.')
        return redirect('products')

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['customer'])])
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        context = {'product_name': product.name,
                   'product_pic': product.product_pic,
                   'product_price': product.price,
                   'new_order_form': self.form_class(initial={'quantity': 1})}
        return render(request, 'accounts/order_form.html', context)


class UpdateOrder(View):
    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def post(self, request, pk):
        order = Order.objects.get(id=pk)
        OrderUpdate(request, order).update_order()
        messages.success(request, 'Order Successfully Updated')
        return redirect('admin_page')

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        form = UpdateOrderForm(instance=order)

        context = {'product': order.product,
                   'update_form': form,
                   'order_quantity': order.quantity}
        return render(request, 'accounts/order_update.html', context)


class DeleteOrder(View):
    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['customer'])])
    def post(self, request, pk):
        order = Order.objects.get(id=pk)
        authorized = is_user_authorized_to_visit_page(request.user,
                                                      order.customer.id)
        if not authorized:
            msg = "You're Not Authorized to Change This Order"
            messages.error(request, msg)
            return redirect('customer', customer_id=request.user.id, page='1')

        deleter = OrderDeleter(order)
        deleter.delete_order()
        status = deleter.get_delete_status()
        if status['status'] == 'success':
            messages.success(request, status['msg'])
            return redirect('customer', customer_id=request.user.id, page='1')
        else:
            messages.error(request, status['msg'])
            return redirect('customer', customer_id=request.user.id, page='1')

    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['customer'])])
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        authorized = is_user_authorized_to_visit_page(request.user,
                                                      order.customer.id)
        if not authorized:
            msg = "You're Not Authorized to Change This Order"
            messages.error(request, msg)
            return redirect('customer', customer_id=request.user.id, page='1')

        context = {'item': order}
        return render(request, 'accounts/delete_order.html', context)


class ShowOrders(View):
    @method_decorator([login_required(login_url='login'),
                       allowed_user(allowed_roles=['admin'])])
    def get(self, request, page):
        page = int(page)
        lister = OrdersListAdmin(request, page)
        orders = lister.get_orders()
        filter_form = OrderFilterForm(initial=request.GET)
        context = {'orders': orders,
                   'page': page,
                   'next_page': page + 1,
                   'prev_page': page - 1,
                   'pages_count': lister.count_pages(),
                   'filter_form': filter_form}
        return render(request, 'accounts/order_all.html', context)
