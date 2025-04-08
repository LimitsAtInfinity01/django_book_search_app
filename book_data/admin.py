from django.contrib import admin
from .models import Profile, Reviews, ReadingList, Comments

# Register your models here.
admin.site.register(Profile)
admin.site.register(Reviews)
admin.site.register(ReadingList)
admin.site.register(Comments)