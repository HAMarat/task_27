from django.urls import path
from rest_framework import routers

from ads import views

router = routers.SimpleRouter()
router.register("", views.AdViewSet)

urlpatterns = [
    path('<int:pk>/upload_image/', views.AdImageView.as_view())
]

urlpatterns += router.urls
