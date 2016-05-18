from django.contrib import admin
from .models import TwitterData, Sentiment

# Register your models here.

admin.site.register(TwitterData)
admin.site.register(Sentiment)