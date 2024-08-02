#user
#profile
#cred
#group
#shareinfo

from django.db import models
from django.contrib.auth.models import User, Group

class AppCredentials(models.Model):
    app_name = models.CharField(max_length=100)
    app_url = models.CharField(max_length=1000,null=True, blank=True)
    app_username = models.CharField(max_length=100, null=True, blank=True)
    app_password = models.CharField(max_length=100,null=True, blank=True)
    app_two_fa = models.CharField(max_length=1000, blank=True, null=True)
    app_note = models.CharField(max_length=3000, blank=True, null=True)

    app_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apps')
    admin_with_users = models.ManyToManyField(User, related_name='app_admins', blank=True)

    shared_with_users = models.ManyToManyField(User, related_name='shared_apps', blank=True)
    shared_with_groups = models.ManyToManyField(Group, related_name='shared_apps', blank=True)

    def __str__(self):
        return self.app_name