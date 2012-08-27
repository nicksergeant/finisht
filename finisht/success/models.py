from django.contrib.auth.models import User
from django.db import models

class Success(models.Model):
    description = models.TextField(max_length=250)
    completed_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name_plural = "Successes"

    def __unicode__(self):
        return u'%s' %(self.description)
