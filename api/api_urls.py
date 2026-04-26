from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)
from apps.users.routes import (user_urls, auth_urls, groups_urls, permissions_urls)
from apps.testimonials.routes import testimonio_urls
from apps.casos_exito.routes import caso_exito_urls
from apps.contacto.routes import contacto_urls
from apps.sepomex.routes import sepomex_urls
from apps.catalogs.routes import catalogs_urls
from apps.propiedades.routes import propiedades_urls

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path("auth/token/", TokenObtainSlidingView.as_view()),
    path("auth/token/refresh/", TokenRefreshSlidingView.as_view()),
    path("user/", include(user_urls)),
    path("auth/", include(auth_urls)),
    path("group/", include(groups_urls)),
    path("permission/", include(permissions_urls)),
    path("testimonial/", include(testimonio_urls)),
    path("caso-exito/", include(caso_exito_urls)),
    path("contacto/", include(contacto_urls)),
    path("sepomex/",   include(sepomex_urls)),
    path("catalogs/",    include(catalogs_urls)),
    path("propiedades/", include(propiedades_urls)),
]
