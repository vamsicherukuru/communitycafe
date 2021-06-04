from django.forms import ModelForm, fields
from django import forms
from .models import *
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': 'form-textbox validate[required]'}), label="", required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}), label="", required=False)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username'}), label="", required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), label="", required=True)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email-id'}), label="", required=True)

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')


class UserProfileForm(forms.ModelForm):
    Area_Name = forms.ModelChoiceField(queryset=Area.objects.all(), widget=forms.Select(
        attrs={'class': 'form-textbox form-address-line'}), label="")

    class Meta():
        model = UserProfile
        fields = ('Area_Name',)
# form-textbox validate[required, Fill Mask]


class CommunityRequestForm(forms.ModelForm):

    class Meta():
        model = CommunityRequests
        exclude = ('user', 'accepted',)


class CreateCommunityForm(forms.ModelForm):

    class Meta():
        model = Community
        exclude = ('admin', 'people')


class busRegForm(forms.ModelForm):

    class Meta():
        model = businessReg
        exclude = ('owner', 'verified',)


class busVerForm(forms.ModelForm):

    class Meta():
        model = businessVerification
        exclude = ('businessname',)


class TravelsUserBookingForm(forms.ModelForm):
    class Meta():
        model = TravelsUserBooking
        exclude = ('customer',)


class RestaurantItemsForm(forms.ModelForm):
    item_name = forms.CharField(required=True)
    price_per_unit = forms.IntegerField(required=True)

    class Meta():
        model = RestaurantItems
        exclude = ('hotel',)


class givebackForm(forms.ModelForm):
    class Meta():
        model = GiveBackReg
        exclude = ('owner_name',)


# Hobbies and skills
class groupRegForm(forms.ModelForm):

    class Meta():
        model = GroupsReg
        exclude = ('admin', 'verified',)


class GroupRequestForm(forms.ModelForm):

    class Meta():
        model = GroupRequests
        exclude = ('user', 'accepted',)


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('body', 'name', 'post')
        labels = {
            "body": "Comment"
        }
        widgets = {'body': forms.Textarea(
            attrs={'rows': 1}), 'name': forms.HiddenInput(), 'post': forms.HiddenInput()}
