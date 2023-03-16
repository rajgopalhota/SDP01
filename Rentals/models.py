# from socket import SOL_NETROM
from xmlrpc.client import DateTime
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now


class RidesRightNow(models.Model):
    user_name = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    cartype = models.CharField(max_length=100)
    phone = models.CharField(max_length=60)

    def __str__(self):
        return 'From: '+self.source+' To: '+self.destination+' User: '+self.user_name


class BookedForLater(models.Model):
    user_name = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    cartype = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return 'Date of travel: '+self.date+' User: '+self.user_name


class FeedbackDB(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
