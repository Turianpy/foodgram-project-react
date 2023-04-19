from django.urls import include, path
from rest_framework import routers
from recipes import views
from users.views import UserViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include('authentication.urls', namespace='auth')),
]