from django.urls import path
from cc import views



app_name = 'cc'


urlpatterns = [

	path('',views.HomePageView,name='homepage'),
	path('register/',views.RegisterView,name='registerView'),
	path('login/',views.LoginView,name='LoginView'),
	path('members/', views.CommunityMembersView, name='members'),
	path('logout/',views.user_logout,name='Logout'),
	path('index/', views.index, name='index'),
	path('joincommunity/', views.CommunityRequestView,name='CommunityRequestView'),
	path('myrequests/',views.MyRequestsView, name='myrequests'),
	path('myapprovals/<int:id>/', views.MyApprovalsView, name="approvals"),
	path('accept/<id>/<community_id>/<member>', views.acceptjoin, name='acceptjoin'),
	path('marketplace/', views.icecreamshopview, name='ice'),
	path('profile/User/view/',views.UserProfilePage,name='profilepage'),
	path('newCommunity/', views.newCommunity, name="createCommunity"),
	path('otp_send/<id>/', views.otp_verify, name='otp_page'),
	path('busReg/',views.busReg,name ='busReg'),
	path('searching/',views.searching,name ='searching'),
    path('business/<int:id>/',views.detail,name ='detail'),
    path('busVer/<int:id>',views.busVer,name='busVer'),
    path('businessListView/', views.BusinessListView, name='buslist' ),
    path('Food/<int:id>/', views.FoodItemDetailView, name='foodde'),
    path('hotel/home/', views.HotelHomeView, name='hotelhome'),
    path('add/cart/<int:id>/', views.AddToCart,name='addToCart'),
    path('cart/view/', views.CartView, name='CartView'),
    path('cart/view/up/<int:id>/<ac>',views.IncreaseQuantity, name='incQ'),
    path('community/posts/<int:id>', views.CommunityPostHomeView, name='composthome'),
    path('community/posts/<int:id>/new/', views.CommunityPostFormView, name='newpost'),
    path('processcheckout/<int:id>/', views.ProcessOrderView, name='processcheckout'),
    path('myOrders/', views.MyOrdersView, name='myorders'),
    path('homebusiness/home/', views.HomeBusinessHomeView, name='homebusinesshome'),
    path('marketplace/home/', views.MarketPlaceHomeView, name='marketplacehome'),
    path('myOrders/order/<int:id>/<user>/', views.OrdersDetail, name='orderdetail'),
    path('add/item/<int:id>/', views.AddRestaurantItemsView, name='additems'),
    path('homechef/food/available/today/<int:id>/', views.ManageTodaysMenuView, name='manage_today'),
    # path('update_item/', views.updateItem,name="update_item"),

    path('makeAvailable/<int:id>/', views.MakeAvailable, name='makeavailable'),
    path('makeunAvailable/<int:id>/', views.MakeUnAvailable, name='makeunavailable'),
    path('giveback/registration/',views.givebackView,name ='gbReg'),
    path('giveback/home/', views.gbHomeView, name='givebackhome'),


    
    #Hobbies and Skills Urls
    path('hobbies/',views.groups,name='groups'),
    path('hobbies/groupsreg/', views.groupReg, name='groupReg'),
    path('hobbies/groups/<int:id>/',views.group_detail,name='group_detail'),
    path('hobbies/groups/posts/<int:id>/new/', views.GroupPostFormView, name='newgrouppost'),
    path('group_requests/',views.UserRequestsView, name='group_requests'),
    path('hobbies/GroupRequestView',views.GroupRequestView, name='GroupRequestView'),
    path('groupapprovals/<int:id>/', views.GroupApprovalsView, name="approvals"),
    path('accept/<id>/<group_id>/<member>', views.groupjoin, name='groupjoin'),
    ]
