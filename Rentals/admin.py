from django.contrib import admin
from .models import BookedForLater,RidesRightNow, FeedbackDB
# Register your models here.

admin.site.register(RidesRightNow)
admin.site.register(BookedForLater)
admin.site.register(FeedbackDB)