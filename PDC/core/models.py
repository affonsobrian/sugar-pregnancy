import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phone_field import PhoneField

from core.Injection import inject_user

inject_user()


class State(models.Model):
    name = models.CharField(max_length=80, unique=True)
    representation = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f"{self.name} - {self.representation}"


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crm = models.IntegerField(null=False, blank=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Hospital(models.Model):
    name = models.CharField(max_length=140)
    address = models.TextField()
    phone = PhoneField(blank=True, null=True)
    doctors = models.ManyToManyField(Doctor)

    def __str__(self):
        return self.name


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True)
    gestational_diabetes_history = models.BooleanField(null=True)
    familiar_diabetes_history = models.BooleanField(null=True)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    acanthosis = models.BooleanField(null=True)
    gestational_parity = models.IntegerField(choices=[(0, "Primeira"), (1, "Multipla")], null=True)
    doctors = models.ManyToManyField(Doctor, related_name="patients", related_query_name="patient",)

    def __str__(self):
        return self.user.get_full_name()


class GlycemicMeasurement(models.Model):
    class Meta:
        unique_together = (('date', 'patient',),)

    date = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    measurement = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.patient.user.get_full_name()}"


class RequestManagement(models.Model):
    class Meta:
        unique_together = ("user", "doctor")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    accepted = models.BooleanField(default=False)
    invite_code = models.UUIDField(default=uuid.uuid4)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(RequestManagement, self).save(*args, **kwargs)
