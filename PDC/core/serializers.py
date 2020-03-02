from django.contrib.auth.models import User, Group
from rest_framework import serializers

from core.models import State, Doctor, Hospital, Patient, GlycemicMeasurement


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'password']
        required = ['password']

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


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
        fields = ['url', 'user', 'crm', 'state', 'patients']


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hospital
        fields = ['url', 'name', 'address', 'phone', 'doctors']


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = ['url', 'user', 'birthday', 'gestational_diabetes_history',
                  'familiar_diabetes_history', 'height', 'weight', 'acanthosis',
                  'gestational_parity', 'doctors']


class GlycemicMeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GlycemicMeasurement
        fields = ['url', 'date', 'patient', 'measurement']
