from django.contrib import admin
from .models import BookedForLater,RidesRightNow
# Register your models here.

admin.site.register(RidesRightNow)
admin.site.register(BookedForLater)