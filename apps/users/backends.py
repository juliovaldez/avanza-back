from django.contrib.auth.backends import ModelBackend
from apps.users.models import User


class EmailOrUsernameBackend(ModelBackend):
    """
    Permite autenticarse con email o con username.
    simplejwt envía el campo `username`; si el valor contiene '@'
    se interpreta como email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return None

        try:
            if "@" in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            User().set_password(password)  # mitigación de timing attack
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
