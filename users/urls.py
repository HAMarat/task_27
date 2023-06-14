from django.urls import path
from rest_framework import routers

from users import views
from users.views import LocationView

router = routers.SimpleRouter()
router.register("location", LocationView)

urlpatterns = [
    path('user/', views.UserListView.as_view()),
    path('user/<int:pk>/', views.UserDetailView.as_view()),
    path('user/create/', views.UserCreateView.as_view()),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view()),
]

urlpatterns += router.urls

