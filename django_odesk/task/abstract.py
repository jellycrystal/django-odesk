from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django_odesk.core import clients

def _odesk_username(django_user):
    return django_user.username.replace('@odesk.com', '')

class BaseTask(models.Model):

    class Meta:
        abstract = True

    code = models.CharField(max_length=16)
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return u"%d: %s/%s" % (self.pk, self.code, self.title)

    def odesk_task_code(self):
        return self.code

    def odesk_task_title(self):
        return self.title

    def odesk_task_owner(self):
        return self.owner

    def odesk_task_url(self):
        return 'http://' + Site.objects.get_current().domain + \
            self.get_absolute_url()

    def odesk_task_company(self):
        return settings.ODESK_TASK_COMPANY

    def odesk_task_team(self):
        return settings.ODESK_TASK_TEAM

    def create_odesk_task(self, odesk_client=None):
        if odesk_client is None:
            odesk_client = clients.UserClient(self.odesk_task_owner())
        odesk_client.otask.post_user_task(
            self.odesk_task_company(),
            self.odesk_task_team(),
            _odesk_username(self.odesk_task_owner()),
            self.odesk_task_code(),
            self.odesk_task_title(),
            self.odesk_task_url())

    def delete_odesk_task(self, odesk_client=None):
        if odesk_client is None:
            odesk_client = clients.UserClient(self.odesk_task_owner())
        odesk_client.otask.delete_user_task(
            self.odesk_task_company(),
            self.odesk_task_team(),
            _odesk_username(self.odesk_task_owner()),
            [self.odesk_task_code()])
