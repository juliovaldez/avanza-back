from rest_framework.routers import DefaultRouter
from apps.testimonials.api.viewsets import TestimonioViewSet

router = DefaultRouter()
router.register("", TestimonioViewSet)

testimonio_urls = router.urls
