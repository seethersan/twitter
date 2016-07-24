from django.contrib.auth.models import User, Group
from rest_framework import serializers
from twitlike.models import Tweet, UserProfile

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
	"""docstring for UserProfileSerializer"""
	user = UserSerializer()

	class Meta(object):
		"""docstring for Meta"""
		model = UserProfile
		fields = ('user','avatar')
			
		



class TweetSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Tweet
		fields = ('user', 'tweet', 'creation_date')