from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)
from apps.users.routes import (user_urls,auth_urls,groups_urls,permissions_urls)
from apps.inventory.routes import (units_urls,
                                   unit_conversion_urls,
                                   status_urls,
                                   location_urls,
                                   inventory_profile_urls,
                                   material_urls,
                                   kit_urls,
                                   transaction_type_urls,
                                   txm_document_urls,
                                   transaction_urls
                                   )

urlpatterns = [
    path("auth/token", TokenObtainSlidingView.as_view()),
    path("auth/token/refresh/", TokenRefreshSlidingView.as_view()),
    path("user/", include(user_urls)),
    path("auth/", include(auth_urls)),
    path("group/", include(groups_urls)),
    path("permission/", include(permissions_urls)),
    path('units/',include(units_urls)),
    path('status/',include(status_urls)),
    path('location/',include(location_urls)),
    path('inventory-profile/',include(inventory_profile_urls)),
    path('material/',include(material_urls)),
    path('unit-conversion/',include(unit_conversion_urls)),
    path('kit/',include(kit_urls)),
    path('transaction-type/',include(transaction_type_urls)),
    path('txn-document/',include(txm_document_urls)),
    path('transaction/',include(transaction_urls)),
]
