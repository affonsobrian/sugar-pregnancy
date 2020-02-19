from django.conf.urls import url
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import State, Doctor, Hospital, Patient, GlycemicMeasurement
from core.serializers import UserSerializer, GroupSerializer, StateSerializer, DoctorSerializer, HospitalSerializer, \
    PatientSerializer, GlycemicMeasurementSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = ()


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = ()


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class GlycemicMeasurementViewSet(viewsets.ModelViewSet):
    queryset = GlycemicMeasurement.objects.all()
    serializer_class = GlycemicMeasurementSerializer
