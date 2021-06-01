from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from cc.models import *
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
import json

# OTP imports

import random 
import http.client
from django.conf import settings
# Create your views here.






def HomePageView(request):

	if request.user.is_authenticated:
		if request.user.userprofile.joined_in_community == False:
			return HttpResponseRedirect(reverse('cc:CommunityRequestView'))


	total_people = int(UserProfile.objects.all().count())
	total_communities = int(Community.objects.all().count())

	return render(request,'basic/home.html',{'total_people':total_people, 'total_communities':total_communities})


# GIVE BACK VIEW
def givebackView(request):
	if request.method == 'POST':
		gb_form=givebackForm(request.POST)
		if gb_form.is_valid():
			gb=gb_form.save(commit=False)
			#gb.owner_name=request.user
			gb.save()
		else:
			print(gb_form.errors)
	else:
		gb_form=givebackForm()
	return render(request,'basic/giveback_registration.html',{'gb_form':gb_form})	

def gbHomeView(request):
	gb=GiveBackReg.objects.all()
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(
			customer=customer, complete=False)
	return render(request, 'basic/gb_items_home.html',{'gb':gb})


def user_logout(request):
	logout(request)

	return HttpResponseRedirect(reverse('cc:homepage'))

def LoginView(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request,user)
				# customer = request.user
				# order, created = Order.objects.get_or_create(customer=customer, complete=False)
				
				return HttpResponseRedirect(reverse('cc:CommunityRequestView'))
			else:
				return HttpResponse("Not an active user")
		else:
			return HttpResponse("not valid credentials")
	else:
		return render(request,'basic/user_login_page.html',{})

def UserProfilePage(request):
	cps = CommunityPosts.objects.all().filter(author=request.user).order_by('-id')


	context = {'cps':cps}
	return render(request,'basic/profilepage.html',context)

def MyApprovalsView(request, id):
	community = Community.objects.get(admin=request.user, id=id)
	my_requests = CommunityRequests.objects.all().filter(Community_Name=community).order_by('-timestamp')
	params = {'my_requests':my_requests}
	return render(request,'basic/myapprovals.html',params)

def acceptjoin(request,id, community_id,member):
	CommunityRequests.objects.filter(id=id).update(accepted=True)

	

	community_add = get_object_or_404(Community, id=community_id)
	community_add.people.add(member), UserProfile.objects.all().filter(user=member).update(joined_in_community=True)

	# pro = UserProfile.objects.get(user=member)
	# pro.joined_in_community = True
	# pro.save()

	# Community.objects.filter(id=id).update(people=people.add(community_requests.user))
	return HttpResponseRedirect(reverse('cc:homepage'))


def AddRestaurantItemsView(request, id):


	if request.method == 'POST':
		add_item_form = RestaurantItemsForm(request.POST)

		if add_item_form.is_valid():
			add_item = add_item_form.save(commit=False)
			current_hotel = businessReg.objects.get(id=id)
			if request.user == current_hotel.owner:
				add_item.hotel = current_hotel

				if 'display_picture' in request.FILES:
					add_item.display_picture = request.FILES['display_picture']
				add_item.save()
				return HttpResponseRedirect(reverse('cc:detail', kwargs={'id':id}))

		#         if 'post_pic' in request.FILES:
		#     newPost.attachment_pic = request.FILES['post_pic']
		# newPost.save()
			else:
				print("not authorized user to add items")

		else:
			print(add_item_form.errors)


	else:
		add_item_form = RestaurantItemsForm()

	return render(request, 'basic/add_restaurant_items.html', {'add_item_form':add_item_form})




def icecreamshopview(request):
	return render(request, 'basic/icecreams_main.html')

# testing payement gateway (for donation page)
def index(request):
	return render(request, "basic/index.html")


@login_required
def MyRequestsView(request):

	my_requests = CommunityRequests.objects.all().filter(user=request.user)
	params = {'my_requests':my_requests}
	return render(request,'basic/myrequests.html',params)


def CommunityRequestView(request):
	registered = False
	if request.method == 'POST':
		community_request_form = CommunityRequestForm(request.POST)
		if community_request_form.is_valid():
			user_join = community_request_form.save(commit=False)
			user_join.user = request.user
			user_join.save()
			registered = True
		else:
			print(community_request_form.errors)
	else:
		community_request_form = CommunityRequestForm()
	return render(request,'basic/communityRegistration.html',{'community_request_form':community_request_form,'registered':registered})


def RegisterView(request):

	# if request.user.is_authenticated:
	#     return HttpResponseRedirect(reverse('ccafe:home'))

	registered = False
	if request.method == 'POST':

		forms_message = request.POST.get('message_form_field')

		if forms_message == 'login_form':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request,user)
					# customer = request.user
					# order, created = Order.objects.get_or_create(customer=customer, complete=False)
					return HttpResponseRedirect(reverse('cc:CommunityRequestView'))

				else:
					return HttpResponse("Not an active user")
			else:
				return HttpResponse("not valid credentials")
		else:


			user_form = UserForm(request.POST)
			profile_form = UserRegistrationForm(request.POST)

			mobile = request.POST.get('mobileNumber')
			customer = request.POST.get('first_name')
			if user_form.is_valid():
			#  and profile_form.is_valid():
				user = user_form.save(commit=False)
				user.set_password(user.password)
				user.is_active = False
				user.save()

			
			
			

			

			

   #          emai_subject = "Activate Your Community Cafe Account"
   #          email_body = "Test cafe"
   #          email = EmailMessage(
   #  		emai_subject,
   #  		email_body,
   #  		settings.EMAIL_HOST_USER,
   #  		[user.email],
			
			
			# )

			
				profile = profile_form.save(commit=False)


			# msg_body = '''
			# 	Hi, Welcome to Community Cafe.


			# 	THANK YOU FOR SIGNING UP

			# 	your account is just one step away to get activated


			# 	Here is your OTP 

			# '''


				profile.user = user
				otp = str(random.randint(1000,9999))
				account_sid = 'AC7d31421e4d0c13f8a64ce6e906e547ee'
				auth_token = 'f1d9d6ffc775498a662e9a4a2aa17849'
				client = Client(account_sid, auth_token)
				message = client.messages.create(
									  body='Hi '+customer+'! \nWELCOME TO COMMUNITY CAFE \nYour Community Cafe Mobile OTP is '+otp,
									  from_='+18707298410',
									  to='+918309756689'
								  )
			
				profile.otp=otp
				if 'profile_pic' in request.FILES:
					profile.profile_pic = request.FILES['profile_pic']
				profile.save()

			# email.send(fail_silently=True)

				registered = True
				user_id = user.id
				return render(request,'basic/activate_your_page.html',{'user_id':user_id})
			# username = request.POST.get('username')
			# password = request.POST.get('password')

			# user = authenticate(username=username, password=password)
			# if user:
			#     if user.is_active:
			#         login(request, user)
			#         return HttpResponseRedirect(reverse('cc:homepage'))
			else:
				print(user_form.errors
				,profile_form.errors)
				a_errors = user_form.errors
				b_errors = profile_form.errors
			   

	else:
		user_form = UserForm()
		profile_form  = UserRegistrationForm()
		a_errors = user_form.errors
		b_errors = profile_form.errors

	return render(request, 'basic/registration.html', {'user_form': user_form, 'profile_form':profile_form ,'registered': registered
																,'a_errors':a_errors,'b_errors':b_errors})



def otp_verify(request, id):


	if request.method=='POST':
		
		otp = request.POST.get('mobile_otp')
		otp = str(otp)

		user = User.objects.get(id=id)

		user_otp = UserProfile.objects.get(user=user)

		if user_otp.otp == otp:
			# User.objects.filter(id=id).update(active=True)
			user.is_active = True
			user.save()
			print("Activated")
			message = "Correct OTP"

			return HttpResponseRedirect(reverse('cc:registerView'))

		else:
			print("not same")

			message = "Wrong OTP"

			return render(request, 'basic/otp.html', {'message':message})






	return render(request, 'basic/otp.html',{})


	



def CommunityMembersView(request):

	allmembers = Community.objects.filter(people__id=request.user.id)

	params = {'members': allmembers}

	return render(request, 'basic/community_members.html',params)


def newCommunity(request):

	if request.method == 'POST':
		community_form = CreateCommunityForm(request.POST)

		if community_form.is_valid():
			community = community_form.save(commit = False)
			community.admin = request.user
			
				# community_add.people.add(member)

			community.save()
			community.people.add(request.user)
			community.save(),UserProfile.objects.all().filter(user=request.user).update(joined_in_community=True)

			return render(request,'basic/community_created.html')

		else:
			print(community_form.errors)
	else:
		community_form = CreateCommunityForm()

	return render(request,'basic/create_community.html',{'community_form':community_form})

def BusinessListView(request):

	business_list = businessReg.objects.filter(owner=request.user)
	context = {'business_list':business_list}
	return render(request,'basic/business_status_view.html', context)


def busReg(request):

	if request.method == 'POST':
		busreg_form = busRegForm(request.POST)
		if busreg_form.is_valid():
			busreg = busreg_form.save(commit = False)
			busreg.owner = request.user
			if 'business_logo' in request.FILES:
				busreg.business_logo = request.FILES['business_logo']

			busreg.save()
# if 'business_logo' in request.FILES:
#                 profile.business_logo = request.FILES['business_logo']
		
		else:
			print(busreg_form.errors)
	else:
		busreg_form = busRegForm()
	return render(request,'basic/business_registration.html',{'busreg_form':busreg_form})



def HotelHomeView(request):
	hotels=businessReg.objects.all().filter(category='Food') 
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(
			customer=customer, complete=False)

	return render(request, 'basic/food_items_home.html',{'hotels':hotels})

def CartView(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(
			customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0}
		cartItems = order['get_cart_items']
	context = {'items': items, 'order': order,'cartItems':cartItems}

	return render(request, 'basic/food_cart.html',context)

def AddToCart(request, id):
	product= RestaurantItems.objects.get(id=id)
	bus_id = product.hotel.id
	order, created = Order.objects.get_or_create(customer=request.user, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order = order,product=product, quantity=1)

	return HttpResponseRedirect(reverse('cc:detail', kwargs={'id':bus_id}))



def IncreaseQuantity(request, id, ac):
	if ac == 'inc':
		product = RestaurantItems.objects.get(id=id)
		order, created = Order.objects.get_or_create(customer=request.user, complete=False)
		orderItem, created = OrderItem.objects.get_or_create(
		order=order, product=product)
		orderItem.quantity = (orderItem.quantity + 1)

		orderItem.save()
		if orderItem.quantity <= 0:
			orderItem.delete()
		return HttpResponseRedirect(reverse('cc:CartView'))

	if ac == 'dec':
		product = RestaurantItems.objects.get(id=id)
		order, created = Order.objects.get_or_create(customer=request.user, complete=False)
		orderItem, created = OrderItem.objects.get_or_create(
		order=order, product=product)
		orderItem.quantity = (orderItem.quantity - 1)

		orderItem.save()
		if orderItem.quantity <= 0:
			orderItem.delete()

		return HttpResponseRedirect(reverse('cc:CartView'))

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(
			customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0}
		cartItems = order['get_cart_items']
	context = {'items': items, 'order': order,'cartItems':cartItems}

	return render(request, 'basic/food_cart.html', context)


# def updateItem(request):

#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']

#     print('Action', action)
#     print('productId:', productId)

#     customer = request.user.customer
#     product = Product.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(
#         customer=customer, complete=False
#     )
#     orderItem, created = OrderItem.objects.get_or_create(
#         order=order, product=product)

#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity + 1)
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity - 1)

#     orderItem.save()

#     if orderItem.quantity <= 0:
#         orderItem.delete()
#     return JsonResponse("Item was added", safe=False)

def MakeAvailable(request, id):

	aa = RestaurantItems.objects.get(id=id)
	aa.available_today = True
	aa.save()

	res_id = aa.hotel.id
	return HttpResponseRedirect(reverse('cc:manage_today', kwargs={'id':res_id}))


def MakeUnAvailable(request, id):

	aa = RestaurantItems.objects.get(id=id)
	aa.available_today = False
	aa.save()

	res_id = aa.hotel.id
	return HttpResponseRedirect(reverse('cc:manage_today', kwargs={'id':res_id}))




def ManageTodaysMenuView(request, id):
	detail_object=businessReg.objects.get(id=id)

	restt = detail_object.id
	all_items = RestaurantItems.objects.all().filter(hotel=restt) 






	return render(request,'basic/manage_today_menu.html', {'all_items':all_items})













def searching(request):
	search_objects=businessReg.objects.all()
	
	category_name=request.GET.get('category_name')
	if category_name != '' and category_name is not None:
		search_objects=search_objects.filter(category__icontains=category_name)

	return render(request,'basic/business_search.html',{'search_object':search_objects})
def FoodItemDetailView(request, id):
	ordered = False
	food_detail = RestaurantItems.objects.get(id=id)
	if request.method == 'POST':
		new_order = RestaurantOrders(user=request.user,hno=request.user.userprofile.houseNumber,area=request.user.userprofile.Area_Name,payment='Done', price=food_detail.price_per_unit, item=food_detail)
		new_order.save()
		ordered = True


	return render(request,'basic/food_item_bill.html',{'food_detail':food_detail, 'ordered':ordered})
def detail(request,id):
	detail_object=businessReg.objects.get(id=id)
	if detail_object.category == 'Travel':
		if request.method == 'POST':
			travel_form = TravelsUserBookingForm(request.POST)
			timeof = request.POST.get('time')
			dateof  =request.POST.get('date')

			travel_form.save(commit=False)
			travel_form.date_of_journey = dateof
			travel_form.time_of_journey = timeof
			travel_form.save()

		else:
			travel_form = TravelsUserBookingForm()
		return render(request, 'basic/business_detail.html',{'travel_form':travel_form})
	if detail_object.category == 'Food':
		restt = detail_object.id
		item_names = RestaurantItems.objects.all().filter(hotel=restt, available_today=True) 
		if request.method == 'POST':
			rest_form = TravelsUserBookingForm(request.POST)
			timeof = request.POST.get('time')
			dateof  =request.POST.get('date')

			travel_form.save(commit=False)
			travel_form.date_of_journey = dateof
			travel_form.time_of_journey = timeof
			travel_form.save()

		else:
			rest_form = TravelsUserBookingForm()
		return render(request, 'basic/restaurant_home.html',{'rest_form':rest_form,'detail_object':detail_object,'items':item_names})

	return render(request,'basic/business_detail.html',{'detail_object':detail_object})


#verification of doc 
def busVer(request, id):
	if request.method == "POST":
		busver_form = busVerForm(request.POST)

		if busver_form.is_valid():
			busver = busver_form.save(commit=False)
			business = businessReg.objects.get(id=id)
			busver.businessname = business
			if 'govid' in request.FILES:
				busver.govid = request.FILES['govid']
		   
			busver.save()
		else:
			print(busver_form.errors)
	else:
		busver_form = busVerForm()


		

	return render(request,'basic/business_verification.html',{'busver_form':busver_form})






def CommunityPostHomeView(request, id):

	community_s = Community.objects.get(id=id)
	cps = CommunityPosts.objects.all().filter(community=community_s).order_by('-id')


	context = {'cps':cps, 'id':community_s.id}


	return render(request, 'basic/community_posts.html', context)



def CommunityPostFormView(request, id):

	if request.method == 'POST':
		title = request.POST.get('title')
		body = request.POST.get('text_body')
		pic = request.POST.get('post_pic')

		community = Community.objects.get(id=id)
		# if 'profile_pic' in request.FILES:
		#             profile.profile_pic = request.FILES['profile_pic']
		newPost = CommunityPosts(title = title, text_body=body, community = community, author=request.user)
		if 'post_pic' in request.FILES:
			newPost.attachment_pic = request.FILES['post_pic']
		newPost.save()


		return HttpResponseRedirect(reverse('cc:composthome',kwargs={'id':id}))


		

	return render(request, 'basic/community_post_form.html', {})



def ProcessOrderView(request, id):

	order = Order.objects.get(id=id)
	order.complete = True
	order.save()

	if request.method == 'POST':

		shipping_address = request.POST.get('new_address')

		new_confirmed_order = ConfirmedOrders(customer=request.user, order=order)
		new_confirmed_order.save()

		return HttpResponseRedirect(reverse('cc:myorders'))


	return render(request, 'basic/processorder.html', {})


def HomeBusinessHomeView(request):

	return render(request, 'basic/homebusinesshome.html',{})

def MarketPlaceHomeView(request):
	return render(request, 'basic/marketplacehome.html',{})

@login_required
def MyOrdersView(request):


	my_completed_orders = ConfirmedOrders.objects.all().filter(customer=request.user).order_by('-timestamp')

	# items = 
	  # customer = request.user
	  #   order, created = Order.objects.get_or_create(
	  #       customer=customer, complete=False)
	  #   items = order.orderitem_set.all()
	context = {'my_completed_orders':my_completed_orders}

	return render(request, 'basic/my_orders.html', context)


@login_required
def OrdersDetail(request, id, user):
	
	order = Order.objects.get(id=id)

	items = order.orderitem_set.all()

	 # order, created = Order.objects.get_or_create(
	 #        customer=customer, complete=False)
	 #    items = order.orderitem_set.all()

	return render(request, 'basic/orders_detail.html', {'items':items})
# Registration Confirmation Email....



# def RegisterView(request):

# 	registered  = False

# 	if request.method == "POST":
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')
# 		mobile_number = request.POST.get('mobilenumber')
# 		houseNo = request.POST.get('hno')
# 		locality = request.POST.get('locality')
# 		area = request.POST.get('area')
# 		city = request.POST.get('city')
# 		state = request.POST.get('state')

# 		new_user = User(username=username,password=password)
		
# 		new_user.set_password(new_user.password)
# 		new_user.save()
# 		new_user_profile = UserProfile(user=new_user,
# 			mobileNumber=mobile_number,
# 			houseNumber = houseNo,
# 			locality = locality,
# 			area = area,
# 			city = city,
# 			state = state
# 			)
# 		new_user_profile.save()

		
# 		template = render_to_string('basic/email_reg_user_confirm.html',

# 		{'name':username}

# 		)
# 		email = EmailMessage(

# 			'Welcome to Community Cafe :);',
# 			template,
# 			settings.EMAIL_HOST_USER,
# 			['cvamsifeb21@gmail.com'],
# 			)

# 		email.fail_silently=False
# 		email.send()
# 		registered = True

# 		return render(request,'basic/registration_successful.html',{registered:'registered'})

	

# 	return render(request,'basic/registration.html',{registered:'registered'})






# HOBBIES AND SKILLS views

def groups(request):
	groups = GroupsReg.objects.all()

	return render(request,'basic/hobbies.html',{'groups':groups})

def groupReg(request):

	if request.method == 'POST':
		groupreg_form = groupRegForm(request.POST)
		if groupreg_form.is_valid():
			groupreg = groupreg_form.save(commit = False)
			groupreg.owner = request.user
			if 'group_logo' in request.FILES:
				groupreg.group_logo = request.FILES['group_logo']

			groupreg.save()
			

		
		else:
			print(groupreg_form.errors)
	else:
		groupreg_form = groupRegForm()
	return render(request,'basic/group_registration.html',{'groupreg_form':groupreg_form})

def group_detail(request,id):
	group_s = GroupsReg.objects.get(id=id)
	gps = GroupPosts.objects.all().filter(group=group_s).order_by('-id')
	detail_object=GroupsReg.objects.get(id=id)
	comment_form = CommentForm(request.POST)
	
	if request.method == 'POST':

		print(request.user)
		form_model = Comment(name=request.user,body=request.POST.get('body'),post=GroupPosts.objects.get(id=int(request.POST.get('id'))))
		form_model.save()
		comment_form = CommentForm()
		return HttpResponseRedirect(reverse('cc:group_detail', kwargs={'id':id}))
			
	else:
		comment_form = CommentForm()

	context = {'gps':gps, 'id':group_s.id,'detail_object':detail_object, 'comment_form':comment_form }
	
	
	return render(request, 'basic/hobbies_group_home.html',context)

# def GroupPostHomeView(request, id):

# 	group_s = GroupsReg.objects.get(id=id)
# 	gps = GroupPosts.objects.all().filter(group=group_s).order_by('-id')


# 	context = {'gps':gps, 'id':group_s.id}


# 	return render(request, 'basic/hobbies_group_home.html', context)



def GroupPostFormView(request, id):

	if request.method == 'POST':
		title = request.POST.get('title')
		body = request.POST.get('text_body')
		pic = request.POST.get('post_pic')

		group = GroupsReg.objects.get(id=id)
		newPost = GroupPosts(title = title, text_body=body, group=group, author=request.user)
		if 'post_pic' in request.FILES:
			newPost.attachment_pic = request.FILES['post_pic']
		newPost.save()


		return HttpResponseRedirect(reverse('cc:group_detail',kwargs={'id':id}))


		

	return render(request, 'basic/group_post_form.html', {})

@login_required
def UserRequestsView(request):

	group_requests = GroupRequests.objects.all().filter(user=request.user)
	params = {'group_requests':group_requests}
	return render(request,'basic/group_requests.html',params)

def GroupRequestView(request):
	registered = False
	if request.method == 'POST':
		group_request_form = GroupRequestForm(request.POST)
		if group_request_form.is_valid():
			user_join = group_request_form.save(commit=False)
			user_join.user = request.user
			user_join.save()
			registered = True
		else:
			print(group_request_form.errors)
	else:
		group_request_form = GroupRequestForm()
	return render(request,'basic/groupjoin.html',{'group_request_form':group_request_form,'registered':registered})

def GroupApprovalsView(request, id):
	group = GroupsReg.objects.get(admin=request.user, id=id)
	group_requests = GroupRequests.objects.all().filter(groupname=group).order_by('-timestamp')
	params = {'group_requests':group_requests}
	return render(request,'basic/groupapprovals.html',params)


def groupjoin(request,id, group_id,member):
	GroupRequests.objects.filter(id=id).update(accepted=True)
	group_add = get_object_or_404(GroupsReg, id=group_id)
	group_add.people.add(member), UserProfile.objects.all().filter(user=member).update(joined_in_group=True)

	# pro = UserProfile.objects.get(user=member)
	# pro.joined_in_community = True
	# pro.save()

	# Community.objects.filter(id=id).update(people=people.add(community_requests.user))
	return HttpResponseRedirect(reverse('cc:homepage'))
