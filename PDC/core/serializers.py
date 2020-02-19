from django.contrib.auth.models import User, Group
from rest_framework import serializers

from core.models import State, Doctor, Hospital, Patient, GlycemicMeasurement


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ['url', 'name', 'representation']


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Doctor
        fields = ['url', 'user', 'crm', 'state']


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hospital
        fields = ['url', 'name', 'address', 'phone', 'doctors']


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = ['url', 'user', 'birthday', 'gestational_diabetes_history',
                  'familiar_diabetes_history','height', 'weight', 'acanthosis',
                  'gestational_parity']


class GlycemicMeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GlycemicMeasurement
        fields = ['url', 'date', 'patient', 'measurement']
