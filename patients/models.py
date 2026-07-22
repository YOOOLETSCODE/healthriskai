from django.db import models
from django.conf import settings

# Create your models here.
class HealthRecord(models.Model):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    smoking_choices = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    exercise_choices = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
    ]
    alcohol_choices = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    family_history_choices = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]   
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='health_records'
    )
    age = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=10, choices=gender_choices)
    smoking = models.CharField(max_length=3, choices=smoking_choices)
    exercise = models.CharField(max_length=10, choices=exercise_choices)
    alcohol = models.CharField(max_length=3, choices=alcohol_choices)
    family_history = models.CharField(max_length=3, choices=family_history_choices)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    bmi = models.FloatField()
    blood_pressure = models.CharField(max_length=7, help_text="Blood Pressure in mmHg (e.g., 120/80)")
    cholesterol = models.FloatField(help_text="Cholesterol in mg/dL")
    glucose = models.FloatField(help_text="Glucose in mg/dL")
    sleep = models.FloatField(help_text="hours per day")
    diabetes_prediction= models.CharField(max_length=20, blank=True, null=True)
    diabetes_confidence= models.FloatField(blank=True, null=True)
    pregnancies = models.PositiveIntegerField(default=0)
    skin_thickness = models.FloatField(default=0.0)
    insulin = models.FloatField(default=0.0)
    diabetes_pedigree_function = models.FloatField(default=0.0)
    def __str__(self):
        return f"Health Record for {self.user.username} - {self.created_at.date()}"