"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from twitlike import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'tweets', views.TweetViewSet)
router.register(r'profiles', views.UserProfileViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'twitlike.views.index'), # root    
    url(r'^login$', 'twitlike.views.login_view'),
    url(r'^logout$', 'twitlike.views.logout_view'),
    url(r'^ascendente$', 'twitlike.views.ascendente'),
    url(r'^decendente$', 'twitlike.views.decendente'),
    url(r'^users/(?P<username>\w{0,30})/$', 'twitlike.views.users'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
