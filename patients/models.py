from django.db import models
from django.conf import settings


class HealthRecord(models.Model):

    gender_choices = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    smoking_choices = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    exercise_choices = [
        ("Low", "Low"),
        ("Moderate", "Moderate"),
        ("High", "High"),
    ]

    alcohol_choices = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    family_history_choices = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="health_records",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    age = models.PositiveIntegerField()

    gender = models.CharField(max_length=10, choices=gender_choices)

    smoking = models.CharField(max_length=3, choices=smoking_choices)

    exercise = models.CharField(max_length=10, choices=exercise_choices)

    alcohol = models.CharField(max_length=3, choices=alcohol_choices)

    family_history = models.CharField(
        max_length=3,
        choices=family_history_choices,
    )

    height = models.FloatField(help_text="Height in cm")

    weight = models.FloatField(help_text="Weight in kg")

    bmi = models.FloatField()

    blood_pressure = models.IntegerField(
        help_text="Systolic blood pressure in mmHg",
    )

    cholesterol = models.FloatField()

    glucose = models.FloatField()

    sleep = models.FloatField(help_text="Hours per day")

    pregnancies = models.PositiveIntegerField(default=0)

    skin_thickness = models.FloatField(default=0)

    insulin = models.FloatField(default=0)

    diabetes_pedigree_function = models.FloatField(default=0)

    # AI Prediction
    diabetes_prediction = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    # Confidence of predicted class
    diabetes_confidence = models.FloatField(
        blank=True,
        null=True,
    )

    # NEW
    diabetic_probability = models.FloatField(default=0,)

    # NEW
    non_diabetic_probability = models.FloatField(default=0,)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"