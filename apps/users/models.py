from django.db import models
from typing import Any
from django.contrib.auth.models import (
        AbstractUser,
    BaseUserManager,
)
import uuid
from api.common.base_models import (TimeStampedModel,SoftDeleteModel,NotDeletedQuerySet,BaseManager,BaseModel)

class UserManager(BaseUserManager):
    def get_queryset(self) -> models.QuerySet:
        return NotDeletedQuerySet(self.model).default()
    
    def _create_user(self,username, email,first_name, password=None,**extra_fields):
        extra_fields.setdefault('pass_token', str(uuid.uuid4()))
        email = self.normalize_email(email)
        user: User = self.model(username=username, email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create(self, **extra_fields: Any) -> Any:
        return self.create_user(**extra_fields)

    def create_user(self, username, email,first_name, password=None,**extra_fields):
        return self._create_user(username, email, first_name, password, **extra_fields)

    def create_superuser(self, username, email,first_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, first_name,password, **extra_fields)



class User(AbstractUser, TimeStampedModel,SoftDeleteModel):
    first_name = models.CharField(max_length=30, blank=False, null=False)  
    email = models.EmailField(unique=True)
    pass_token=models.CharField(max_length=255,blank=True,null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email","first_name"]
    FILTER_SORT_ORDER_FIELDS=["id","first_name","email","groups"]
    
    class Meta:
        ordering=['-id']

    def __str__(self):
        return self.email
    
    def reset_pass_token(self):
        self.pass_token = str(uuid.uuid4())
        self.save()



