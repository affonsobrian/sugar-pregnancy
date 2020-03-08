from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import State, Doctor, Hospital, Patient, GlycemicMeasurement
from core.serializers import UserSerializer, GroupSerializer, StateSerializer, DoctorSerializer, HospitalSerializer, \
    PatientSerializer, GlycemicMeasurementSerializer, AcceptRequestManagementSerializer

from core.permission.permissions import IsAuthenticatedOrWriteOnly, ChangeItSelfOnly, IsDoctor, IsPatient, IsNotDoctor

from core.models import RequestManagement
from core.serializers import RequestManagementSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrWriteOnly,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = ()


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = (IsAuthenticated, ChangeItSelfOnly)


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = (IsAuthenticated,)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_doctor():
            return self.request.user.doctor.patients.all()
        if self.request.user.is_patient():
            return Patient.objects.filter(id=self.request.user.patient.id)
        return Patient.objects.none()


class GlycemicMeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = GlycemicMeasurementSerializer
    queryset = GlycemicMeasurement.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor():
            return GlycemicMeasurement.objects.filter(patient__in=user.doctor.patients.all())
        if user.is_patient():
            return GlycemicMeasurement.objects.filter(patient=user.patient)
        return GlycemicMeasurement.objects.none()


class AcceptRequestManagementViewSet(viewsets.ModelViewSet):
    serializer_class = AcceptRequestManagementSerializer
    queryset = RequestManagement.objects.all()
    permission_classes = (IsDoctor,)

    def get_queryset(self):
        return RequestManagement.objects.filter(doctor=self.request.user.doctor, accepted=False).order_by('created_at')


class RequestManagementViewSet(viewsets.ModelViewSet):
    serializer_class = RequestManagementSerializer
    queryset = RequestManagement.objects.all()
    permission_classes = (IsNotDoctor,)

    def get_queryset(self):
        return RequestManagement.objects.filter(user=self.request.user)

