from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField


class State(models.Model):
    name = models.CharField(max_length=80, unique=True)
    representation = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f"{self.name} - {self.representation}"


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crm = models.IntegerField(null=False, blank=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE)


class Hospital(models.Model):
    name = models.CharField(max_length=140)
    address = models.TextField()
    phone = PhoneField(blank=True, null=True)
    doctors = models.ManyToManyField(Doctor)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    gestational_diabetes_history = models.BooleanField()
    familiar_diabetes_history = models.BooleanField()
    weight = models.FloatField()
    height = models.FloatField()
    acanthosis = models.BooleanField()
    gestational_parity = models.IntegerField(choices=[(0, "Primeira"), (1, "Multipla")])
    doctors = models.ManyToManyField(Doctor, related_name="patients", related_query_name="patient",)

    def __str__(self):
        full_name = f"{self.user.first_name}  {self.user.last_name}"
        if full_name.replace(" ", ""):
            return full_name
        return self.user.email


class GlycemicMeasurement(models.Model):
    class Meta:
        unique_together = (('date', 'patient',),)

    date = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    measurement = models.FloatField()

