"""
Google OAuth 2.0 — Authorization Code Flow
-------------------------------------------
El frontend envía el code recibido de Google.
Este endpoint:
  1. Intercambia el code por tokens usando el client_secret (nunca expuesto al frontend).
  2. Verifica criptográficamente el id_token con las claves públicas de Google.
  3. Valida que el email esté verificado por Google.
  4. Obtiene o crea el usuario local.
  5. Devuelve un SlidingToken idéntico al login normal.
"""
import requests as http_client

from django.conf import settings
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import SlidingToken

from apps.users.models import User
from api.utils.utils import json_response

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


@api_view(["POST"])
@permission_classes([AllowAny])
def google_login(request):
    """
    Body esperado: { "code": "...", "redirect_uri": "..." }
    """
    code         = request.data.get("code", "").strip()
    redirect_uri = request.data.get("redirect_uri", "").strip()

    if not code or not redirect_uri:
        return Response(
            {"detail": "Se requieren 'code' y 'redirect_uri'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ── 1. Intercambiar code por tokens de Google ──────────────────────────
    token_response = http_client.post(
        GOOGLE_TOKEN_URL,
        data={
            "code":          code,
            "client_id":     settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri":  redirect_uri,
            "grant_type":    "authorization_code",
        },
        timeout=10,
    )

    if token_response.status_code != 200:
        return Response(
            {"detail": "No se pudo completar la autenticación con Google."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token_data = token_response.json()
    raw_id_token = token_data.get("id_token")

    if not raw_id_token:
        return Response(
            {"detail": "Google no devolvió un id_token válido."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ── 2. Verificar id_token criptográficamente con las claves de Google ──
    try:
        claims = google_id_token.verify_oauth2_token(
            raw_id_token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except ValueError as exc:
        return Response(
            {"detail": f"Token de Google inválido: {exc}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ── 3. Validar que el email esté verificado por Google ─────────────────
    if not claims.get("email_verified"):
        return Response(
            {"detail": "El correo de Google no está verificado."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    email      = claims.get("email", "").lower()
    first_name = claims.get("given_name", "")
    last_name  = claims.get("family_name", "")

    if not email:
        return Response(
            {"detail": "No se pudo obtener el correo desde Google."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ── 4. Obtener o crear usuario ──────────────────────────────────────────
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username":   email,
            "first_name": first_name,
            "last_name":  last_name,
        },
    )

    # Si el usuario existe pero no tiene nombre, actualizarlo
    if not created and (not user.first_name or not user.last_name):
        user.first_name = user.first_name or first_name
        user.last_name  = user.last_name  or last_name
        user.save(update_fields=["first_name", "last_name"])

    # ── 5. Emitir SlidingToken (igual que el login normal) ─────────────────
    sliding_token = SlidingToken.for_user(user)

    return json_response(
        data={"token": str(sliding_token)},
        message="Autenticación con Google exitosa.",
    )
