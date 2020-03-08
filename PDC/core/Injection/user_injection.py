from django.contrib.auth.models import User


def is_doctor(self):
    from core.models import Doctor
    has = hasattr(self, 'doctor')
    return bool(has and isinstance(self.doctor, Doctor))


def is_patient(self):
    from core.models import Patient
    has = hasattr(self, 'patient')
    return bool(has and isinstance(self.patient, Patient))


User.is_doctor = is_doctor
User.is_patient = is_patient


def inject_user():
    User.is_doctor = is_doctor
    User.is_patient = is_patient
