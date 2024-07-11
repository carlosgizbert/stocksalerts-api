from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from prostocks.views import UserCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("panel/", include("stocks.urls")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserCreateAPIView.as_view(), name='user'),
]
