from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorates import unauthrised_user,allowed_users,admin_only

#Create your view here
from .models import *
from .forms import Orderform, CreatUserForm,CustomerCreationForm
from .filters import OrderFilter

# Create your views here.
@unauthrised_user
def loginPage(request):

		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
			else :
				messages.info(request,'Username or Password is incorrect!')
		context = {}
		return render(request,'accounts/login.html',context)
def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userprofile(request):
	orders = request.user.customer.order_set.all()

	ord_cout = orders.count()
	deliver_cout = orders.filter(status="Delivered").count()
	pending_cout = orders.filter(status="Pending").count()

	#print("Orders:".orders)
	context={'orders':orders,'ord_cout':ord_cout,'deliver_cout':deliver_cout,'pending_cout':pending_cout}

	return render(request,'accounts/user_profile.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_settings(request):
	customer = request.user.customer
	form = CustomerCreationForm(instance=customer)
	if request.method =='POST':
		form = CustomerCreationForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save()
			return redirect('user-settings')
	context= {'form':form}
	return render(request, 'accounts/user_settings.html',context)


@unauthrised_user
def registration(request):

		userRegForm = CreatUserForm()
		print(userRegForm)
		if request.method == 'POST':
			form = CreatUserForm(request.POST)

			if form.is_valid():
				user = form.save()

				username = form.cleaned_data.get('username')

				group = Group.objects.get(name='customer')
				user.groups.add(group)
				# Added username after video because of error returning customer name if not added
				Customer.objects.create(
					user=user,
					name=user.username,
				)

				messages.success(request, 'Account was created for ' + username)

				return redirect('login')

		context = {'form':userRegForm}

		return render(request,'accounts/registration.html',context)

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	ord_cout = orders.count()
	deliver_cout = orders.filter(status="Delivered").count()
	pending_cout = orders.filter(status="Pending").count()

	context = {'orders':orders,'customers':customers,'ord_cout':ord_cout,'deliver_cout':deliver_cout,'pending_cout':pending_cout}
	return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	context = {'products':products}
	return render(request,'accounts/product.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request,pk_id):

	customer = Customer.objects.get(id=pk_id)
	orders = customer.order_set.all() #_set Returns all child models related to parent
	order_count = orders.count()

	myFilter = OrderFilter(request.GET,queryset=orders)
	orders = myFilter.qs

	context = {'customer':customer , 'orders':orders , 'order_count' : order_count,'myFilter':myFilter}
	return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request,pk):
	Orderformset = inlineformset_factory(Customer,Order,fields=('product','status'),extra=3)

	customer = Customer.objects.get(id=pk)
	formset = Orderformset(queryset=Order.objects.none(),instance=customer)
	#form = Orderform(initial={'customer':customer})
	if request.method =='POST':
		#print('Printing POST', request.POST)
		form = Orderformset(request.POST,instance=customer)
		if form.is_valid():
			form.save()
			return  redirect('/')
	context = {'formset':formset}
	return render(request,'accounts/create_order.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request,pk):
	order = Order.objects.get(id=pk)
	form = Orderform(instance=order)
	if request.method =='POST':
		form = Orderform(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request,pk):
	order = Order.objects.get(id=pk)
	if request.method=='POST':
		order.delete()
		return redirect('/')
	context = {'item':order}
	return render(request,'accounts/delete.html',context)

