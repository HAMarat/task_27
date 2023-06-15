from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.authtoken import views

from users.views import *

router = routers.SimpleRouter()
router.register("location", LocationView)

urlpatterns = [
    path('user/', UserListView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),
    path('user/create/', UserCreateView.as_view()),
    path('user/<int:pk>/update/', UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', UserDeleteView.as_view()),
    path('user/login/', views.obtain_auth_token),
    path('user/token/', TokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view())
]

urlpatterns += router.urls

