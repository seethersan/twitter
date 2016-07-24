from django.contrib import admin

# Register your models here.

from twitlike.models import Tweet

class TweetAdmin(admin.ModelAdmin):
	list_display = ('user','tweet', 'creation_date')
		
admin.site.register(Tweet, TweetAdmin)