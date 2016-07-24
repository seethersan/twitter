from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from twitlike.forms import AuthenticateForm, UserProfileForm, TweetForm, UpdateProfile
from twitlike.models import Tweet, UserProfile
from twitlike.serializers import UserSerializer, TweetSerializer, UserProfileSerializer
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework import viewsets

# Create your views here.
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')


def ascendente(request):
	order = True
	return index(request, order=order)


def decendente(request):
	order = False
	return index(request, order=order)


def index(request, auth_form=None, user_form=None, order=None):
	if order:
		tweets = Tweet.objects.order_by('-id')
	else:
		tweets = Tweet.objects.order_by('id')
	tweet_form = TweetForm()
	estado = None
	if request.user.is_authenticated():
		if request.method == "POST":
			tweet_form = TweetForm(data=request.POST)
			if tweet_form.is_valid():
				tweet = tweet_form.save(commit=False)
				tweet.user = request.user
				tweet.save()
	else:
		auth_form = auth_form or AuthenticateForm()
		user_form = user_form or UserProfileForm()
		if request.method == "POST":
			user_form = UserProfileForm(data=request.POST)
			if user_form.is_valid():
				username = user_form.cleaned_data['email']
				password = user_form.cleaned_data['password1']
				if not User.objects.filter(email=username):
					user_form.save()
					user = authenticate(username=username, password=password)
					profile = UserProfile.objects.create(user=user)
					login(request, user)
					profile.save()
				else:
					estado = "No registrado"
			else:
				user_form = UserProfileForm()
				return render(request,'index.html',{'tweets':tweets, 'tweet_form': tweet_form, 'auth_form': auth_form, 'user_form': user_form,'username': request.user.username or None, 'estado': estado})
	return render(request,'index.html',{'tweets':tweets, 'tweet_form': tweet_form, 'auth_form': auth_form, 'user_form': user_form,'username': request.user.username or None, 'estado': estado})


def users(request, username="", profile_form=None, profile=None):
	avatar = None
	if username:
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			raise Http404
		tweets = Tweet.objects.filter(user=user.id)
		if username == request.user.username:
			profile_form = UpdateProfile()
			profile = UserProfile.objects.get(user__username=username)
			if request.method == "POST":
				profile_form = UpdateProfile(request.POST, request.FILES)
				if profile_form.is_valid():
					if profile_form.cleaned_data['first_name']:
						user.first_name = profile_form.cleaned_data['first_name']
					if profile_form.cleaned_data['last_name']:
						user.last_name = profile_form.cleaned_data['last_name']
					if profile_form.cleaned_data['last_name'] or profile_form.cleaned_data['first_name']:
						user.save()
					if request.FILES:
						profile.avatar = request.FILES['avatar']
						profile.save()
						avatar = profile.avatar
					else:
						avatar = profile.avatar or None
			else:
				if not profile.avatar:
					return render(request, 'user.html', {'user': user, 'tweets': tweets, 'profile_form': profile_form})
				else:
					avatar = profile.avatar
			return render(request, 'user.html', {'user': user, 'tweets': tweets, 'profile_form': profile_form, 'avatar': avatar})
	else:
		redirect('/')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class TweetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    
