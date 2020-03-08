from django.contrib.auth.models import User, Group
from rest_framework import serializers

from core.models import State, Doctor, Hospital, Patient, GlycemicMeasurement

from core.models import RequestManagement


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'first_name', 'last_name', 'username', 'email', 'groups', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

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
        read_only = ['patients']


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


class RequestManagementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RequestManagement
        fields = ['url', 'user', 'doctor', 'invite_code']
        read_only_fields = ['user']

    def validate(self, attrs):
        attrs = super(RequestManagementSerializer, self).validate(attrs)
        user = self.context['request'].user
        doctor = attrs['doctor']
        search = RequestManagement.objects.filter(user=user, doctor=doctor)
        if search.exists():
            raise serializers.ValidationError("There's a request already, or the doctor is"
                                              " already connected to the given user.")
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        return super(RequestManagementSerializer, self).create(validated_data)


class AcceptRequestManagementSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RequestManagement
        fields = ['invite_code', 'user']
        extra_kwargs = {
            'invite_code': {'required': True}
        }

    def create(self, validated_data):
        request_management = RequestManagement.objects.get(invite_code=validated_data['invite_code'],
                                                           doctor=self.request.user.doctor)
        if request_management.accepted:
            return request_management
        if request_management.user.is_patient():
            p = request_management.user.patient
            p.doctors.add(request_management.doctor)
        else:
            p = Patient()
            p.user = request_management.user
            p.save()
            p.doctors.add(request_management.doctor)
        request_management.accepted = True
        request_management.save()
        return request_management
