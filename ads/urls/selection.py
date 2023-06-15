from rest_framework import routers

from ads import views

router = routers.SimpleRouter()
router.register("", views.SelectionViewSet)

urlpatterns = router.urls
