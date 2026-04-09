from django.contrib import avanza

# Register your models here.
from apps.users.models import User

avanza.site.register(User)
