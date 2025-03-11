from rest_framework.routers import DefaultRouter
from apps.inventory.api.viewsets.unit_viewset import UnitViewSet
from apps.inventory.api.viewsets.status_viewset import StatusViewset
from apps.inventory.api.viewsets.location_viewset import LocationViewSet
from apps.inventory.api.viewsets.inventory_profile_viewset import InventoryProfileViewSet
from apps.inventory.api.viewsets.material_viewset import MaterialViewset
from apps.inventory.api.viewsets.unit_conversion_viewset import UnitConversionViewSet
from apps.inventory.api.viewsets.kit_viewset import KitViewSet
from apps.inventory.api.viewsets.transaction_type_viewset import TransactionTypeViewSet
from apps.inventory.api.viewsets.txn_document_viewset import TxnDocumentViewSet
from apps.inventory.api.viewsets.transaction_viewset import TransactionViewSet




router= DefaultRouter()
router.register("",UnitViewSet)
units_urls = router.urls

router=DefaultRouter()
router.register('',StatusViewset)
status_urls=router.urls

router=DefaultRouter()
router.register('',LocationViewSet)
location_urls=router.urls

router=DefaultRouter()
router.register('',InventoryProfileViewSet)
inventory_profile_urls=router.urls

router=DefaultRouter()
router.register('',MaterialViewset)
material_urls=router.urls

router=DefaultRouter()
router.register('',UnitConversionViewSet)
unit_conversion_urls= router.urls

router=DefaultRouter()
router.register('',KitViewSet)
kit_urls=router.urls

router=DefaultRouter()
router.register('',TransactionTypeViewSet)
transaction_type_urls=router.urls

router=DefaultRouter()
router.register('',TxnDocumentViewSet)
txm_document_urls=router.urls

router=DefaultRouter()
router.register('',TransactionViewSet)
transaction_urls=router.urls




