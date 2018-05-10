from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings
# Create your models here.
class User(AbstractUser):
    touxiang  = models.ImageField(upload_to= "touxiang")
    nickname = models.CharField(max_length=50, blank=True)
    #user = models.OneToOneField(User,)
    class Meta(AbstractUser.Meta):
        pass