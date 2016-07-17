from django import forms
from django.core.files.images import get_image_dimensions
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.utils.html import strip_tags

from twitlike.models import UserProfile, Tweet


class UserProfileForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

    def is_valid(self):
        form = super(UserProfileForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    class Meta:
        fields = ['email','username', 'first_name', 'last_name', 'password1', 'password2']
        model = User


class UpdateProfile(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    avatar = forms.ImageField(label='avatar', required=False)

    def is_valid(self):
        form = super(UpdateProfile, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    class Meta:
        fields = ['first_name', 'last_name', 'avatar']
        model = User


class AuthenticateForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
 
    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form
        

class TweetForm(forms.ModelForm):
    tweet = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'class': 'twitlikeText'}))
 
    def is_valid(self):
        form = super(TweetForm, self).is_valid()
        for f in self.errors.iterkeys():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error twitlikeText'})
        return form
 
    class Meta:
        model = Tweet
        exclude = ('user',)

