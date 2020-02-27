from django.urls import include
from django.contrib import admin
from rest_framework import routers

from core import views

from django.urls import path
from rest_framework_simplejwt import views as jwt_views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'states', views.StateViewSet)
router.register(r'doctors', views.DoctorViewSet)
router.register(r'hospitals', views.HospitalViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'glicemic', views.GlycemicMeasurementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]
