from django.contrib.auth.models import User
from django.db import models

class Friend(models.Model):
    main_user = models.IntegerField()
    friend_user = models.ForeignKey(User)
    pending = models.BooleanField()

    def __unicode__(self):
        return u'%s' %(self.main_user)
