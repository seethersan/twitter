from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your models here.
class Tweet(models.Model):
	tweet = models.CharField(max_length=140)
	user = models.ForeignKey(User)
	creation_date = models.DateTimeField(auto_now=True, blank=True)


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to='static/avatar')

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
