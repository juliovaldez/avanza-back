from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.users.api.serializers.auth_serializers import (
    SetPasswordSerializer,
    ResetPasswordSerializer
)
from api.utils.utils import json_response
from rest_framework_simplejwt.tokens import SlidingToken
from rest_framework.permissions import AllowAny
from apps.users.signals import send_reset_email_signal
from apps.users.models import User

class AuthViewSet(viewsets.GenericViewSet):

    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def logout(self, request: Request) -> Response:
        token = SlidingToken(request.data.get("token"))
        token.blacklist()
        return Response(
            {"status": "user deactivated"}, status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=["post"])
    def set_password(self, request: Request) -> Response:
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return json_response(message="Password updated")
    
    @action(detail=False,methods=['post'])
    def reset_password(self, request:Request)->Response:
        serializer=ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user:User=serializer.save()
        send_reset_email_signal.send(sender=self.__class__,user_id=user.id)
        return json_response(message="Password reset")

