from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from twilio.rest import Client
# from django.contrib.gis.db import models

# Create your models here.
# class City(models.Model):
# 	city_name = models.CharField()


class Pincode(models.Model):
    pincode = models.CharField(
        max_length=6, blank=True, null=True, unique=True)

    def __str__(self):
        return self.pincode


class Area(models.Model):
    Area_Name = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.ForeignKey(
        Pincode, on_delete=models.CASCADE, null=True, blank=True)
    city_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.Area_Name + " (" + self.city_name + ", " + str(self.pincode) + ")"


# class Bookings(mode):
# 	Destination = models.ForeignKey(Pincode, on_delete=models.CASCADE, null=True, blank=True)
# 	Bus = models.ForeignKey(Pincode, on_delete=models.CASCADE, null=True, blank=True)
# 	no_of Seats =


class Community(models.Model):
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    Area_Name = models.ForeignKey(
        Area, on_delete=models.CASCADE, blank=True, null=True)
    # pincode = models.ForeignKey(
    #     Pincode, on_delete=models.CASCADE, null=True, blank=True)
    Community_Name = models.CharField(max_length=200)
    people = models.ManyToManyField(
        User, related_name='community_members', blank=True, null=True)
    # class Meta:
    # 	unique_together = ('user', 'Community_Name',)

    class Meta:
        unique_together = ('admin', 'Area_Name',)

    def total_members(self):
        return self.people.count()

    def __str__(self):
        return self.Community_Name + " (" + str(self.Area_Name.pincode) + ")"
        # + " >> " + str(self.people.count())


class CommunityRequests(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    # Area_Name = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null = True)
    Community_Name = models.ForeignKey(Community, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'Community_Name',)

    def __str__(self):
        return self.user.username + " ___ REQUESTED TO JOIN__" + self.Community_Name.Community_Name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # pincode = models.ForeignKey(Pincode, on_delete=models.CASCADE, null=True, blank=True)
    Area_Name = models.ForeignKey(
        Area, on_delete=models.CASCADE, blank=True, null=True)
    mobileNumber = models.CharField(max_length=10)
    houseNumber = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_choices = (("Andhra Pradesh", "Andhra Pradesh"), ("Arunachal Pradesh ", "Arunachal Pradesh "), ("Assam", "Assam"), ("Bihar", "Bihar"), ("Chhattisgarh", "Chhattisgarh"), ("Goa", "Goa"), ("Gujarat", "Gujarat"), ("Haryana", "Haryana"), ("Himachal Pradesh", "Himachal Pradesh"), ("Jammu and Kashmir ", "Jammu and Kashmir "), ("Jharkhand", "Jharkhand"), ("Karnataka", "Karnataka"), ("Kerala", "Kerala"), ("Madhya Pradesh", "Madhya Pradesh"), ("Maharashtra", "Maharashtra"), ("Manipur", "Manipur"), ("Meghalaya", "Meghalaya"), ("Mizoram", "Mizoram"), ("Nagaland", "Nagaland"), ("Odisha", "Odisha"),
                     ("Punjab", "Punjab"), ("Rajasthan", "Rajasthan"), ("Sikkim", "Sikkim"), ("Tamil Nadu", "Tamil Nadu"), ("Telangana", "Telangana"), ("Tripura", "Tripura"), ("Uttar Pradesh", "Uttar Pradesh"), ("Uttarakhand", "Uttarakhand"), ("West Bengal", "West Bengal"), ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"), ("Chandigarh", "Chandigarh"), ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"), ("Daman and Diu", "Daman and Diu"), ("Lakshadweep", "Lakshadweep"), ("National Capital Territory of Delhi", "National Capital Territory of Delhi"), ("Puducherry", "Puducherry"))

    state = models.CharField(choices=state_choices, max_length=255)
    joined_on = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    joined_in_community = models.BooleanField(default=False)
    active_account = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " __joined on __" + str(self.joined_on)


# Business Registration

class businessReg(models.Model):
    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)

    busChoice = [
        ('Travel', 'Travel'),
        ('Food', 'Food'),
        ('Tutions', 'Tutions'),
        ('Sports', 'Sports'),
    ]
    category = models.CharField(choices=busChoice, default='', max_length=100)
    businessname = models.CharField(max_length=100, blank=True, null=True)
    address = models.ForeignKey(
        Area, on_delete=models.SET_NULL, null=True, blank=True)
    verified = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True, null=True)
    business_logo = models.ImageField(
        upload_to='business_reg_pics', blank=True, null=True)

    def __str__(self):
        return self.businessname + " - " + self.owner.username + ' registered under ' + self.category + ' category'

    class Meta:
        unique_together = ('owner', 'businessname', 'address', 'category')


class RestaurantItems(models.Model):
    hotel = models.ForeignKey(
        businessReg, on_delete=models.CASCADE, blank=True, null=True)
    item_name = models.CharField(max_length=500, blank=True, null=True)
    price_per_unit = models.IntegerField(default=10)
    display_picture = models.ImageField(
        upload_to='food_images', blank=True, null=True)
    available_today = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.hotel.businessname + " - " + self.item_name

    @property
    def imageURL(self):
        try:
            url = self.display_picture.url
        except:
            url = ''
        return url

# details of home business supplier taken to be verified by communitycafe admin


class businessVerification(models.Model):

    businessname = models.ForeignKey(
        businessReg, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=50)
    govid = models.FileField(blank=True, null=True,
                             upload_to='governmentid/%Y/%m/%D/')
    pancard = models.ImageField(
        blank=True, null=True, upload_to='pandetails/%Y/%m/%D/')
    photos = models.ImageField(upload_to='images', blank=True, null=True)
    # mobile

    def __str__(self):
        return self.businessname.owner.username + '\'s Verification Files'


class TravelsUserBooking(models.Model):

    source_choices = [
        ('Hyderabad', 'Hyderabad'),
        ('Bangalore', 'Bangalore'),
        ('Delhi', 'Delhi'),
        ('Mumbai', 'Mumbai'),
    ]
    source = models.CharField(choices=source_choices,
                              max_length=100, default='')

    destination_choices = [
        ('Hyderabad', 'Hyderabad'),
        ('Bangalore', 'Bangalore'),
        ('Delhi', 'Delhi'),
        ('Mumbai', 'Mumbai'),
    ]
    destination = models.CharField(
        choices=destination_choices, max_length=100, default='')
    date_of_journey = models.DateField(blank=True, null=True)
    time_of_journey = models.TimeField(blank=True, null=True)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.customer.username


class RestaurantOrders(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    hno = models.CharField(max_length=100)
    area = models.CharField(max_length=500)
    payment = models.CharField(max_length=100)
    item = models.ForeignKey(
        RestaurantItems, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.item.item_name


# class ConfirmedOrder(models.Model):
# 	customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
# 	complete = models.BooleanField(default=False, null=True, blank=True)
# 	trasaction_id = models.CharField(max_length=200, null=True)
# 	date_ordered = models.DateTimeField(auto_now_add=True, blank=True, null=True)

# 	@property
# 	def get_cart_total(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.get_total for item in orderitems])
# 		return total
# 	@property
# 	def get_cart_items(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.quantity for item in orderitems])
# 		return total

# 	def __str__(self):
# 		return str(self.id)


class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    trasaction_id = models.CharField(max_length=200, null=True)
    date_ordered = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.id)

    # @property
 #    def get_cart_total(self):
 #    	orderitems = self.orderitem_set.all()
 #    	total = sum([item.get_total for item in orderitems])
 #        return total

 #    @property
 #    def get_cart_items(self):
 #        orderitems = self.orderitem_set.all()
 #        total = sum([item.quantity for item in orderitems])
 #        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        RestaurantItems, on_delete=models.SET_NULL, blank=True, null=True)

    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cooking_instruction = models.CharField(
        max_length=500, blank=True, null=True)

    def __str__(self):
        return self.product.item_name

    @property
    def get_total(self):
        total = self.product.price_per_unit * self.quantity
        return total


class CommunityPosts(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(
        Community, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    attachment_pic = models.ImageField(
        upload_to='community_posts_pics', blank=True, null=True)
    text_body = models.TextField(max_length=3000, blank=True, null=True)

    def __str__(self):
        return "Post Number  = " + str(self.id)


class ConfirmedOrders(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    Order_Delivered = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return "Order Number = " + str(self.id)


# Give back model
class GiveBackReg(models.Model):
    owner_name = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    resource_photo = models.ImageField(
        upload_to='give_back_photos', blank=True, null=True)
    resource_description = models.CharField(
        max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=10)
    givebackChoice = [
        ('Share', 'Share'),
        ('Lend', 'Lend'),
        ('Recycle', 'Recycle'),
        ('Donate', 'Donate'),

    ]
    resource = models.CharField(choices=givebackChoice, max_length=100)


# Hobbies And Skills


class GroupsReg(models.Model):
    admin = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)

    groupname = models.CharField(max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True, null=True)
    group_logo = models.ImageField(
        upload_to='group_reg_pics', blank=True, null=True)
    people = models.ManyToManyField(
        User, related_name='group_members', blank=True, null=True)

    def __str__(self):
        return self.groupname

    class Meta:
        unique_together = ('admin', 'groupname',)


class GroupPosts(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(
        GroupsReg, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    attachment_pic = models.ImageField(
        upload_to='group_posts_pics', blank=True, null=True)
    text_body = models.TextField(max_length=3000, blank=True, null=True)

    def __str__(self):
        return "Post Number  = " + str(self.id)


class GroupRequests(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    # Area_Name = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null = True)
    groupname = models.ForeignKey(GroupsReg, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'groupname',)

    def __str__(self):
        return self.user.username + " ___ REQUESTED TO JOIN__" + self.groupname.groupname


class Comment(models.Model):
    post = models.ForeignKey(
        GroupPosts, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
