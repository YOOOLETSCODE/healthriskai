from django.db import models
from django.conf import settings


class HealthRecord(models.Model):

    # ======================
    # CHOICES
    # ======================

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    RACE_CHOICES = [
        ("AfricanAmerican", "African American"),
        ("Asian", "Asian"),
        ("Caucasian", "Caucasian"),
        ("Hispanic", "Hispanic"),
        ("Other", "Other"),
    ]

    SMOKING_CHOICES = [
        ("No Info", "No Info"),
        ("current", "Current"),
        ("ever", "Ever"),
        ("former", "Former"),
        ("never", "Never"),
        ("not current", "Not Current"),
    ]

    # ======================
    # USER
    # ======================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="health_records",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # ======================
    # MODEL INPUT FEATURES
    # ======================

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    race = models.CharField(
        max_length=20,
        choices=RACE_CHOICES,
    )

    hypertension = models.BooleanField(
        null=True,
        blank=True,
    )

    heart_disease = models.BooleanField(
        null=True,
        blank=True,
    )

    bmi = models.FloatField()

    hbA1c_level = models.FloatField(
        verbose_name="HbA1c Level",
    )

    blood_glucose_level = models.FloatField()

    smoking_history = models.CharField(
        max_length=20,
        choices=SMOKING_CHOICES,
    )

    # ======================
    # AI OUTPUT
    # ======================

    diabetes_prediction = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    diabetes_confidence = models.FloatField(
        blank=True,
        null=True,
    )

    diabetic_probability = models.FloatField(
        default=0,
    )

    non_diabetic_probability = models.FloatField(
        default=0,
    )

    # ======================
    # DISPLAY PROPERTIES
    # ======================

    @property
    def hba1c_status(self):
        """
        HbA1c Interpretation
        """
        if self.hbA1c_level < 5.7:
            return "Normal"
        elif self.hbA1c_level < 6.5:
            return "Prediabetes"
        return "High"

    @property
    def glucose_status(self):
        """
        Blood Glucose Interpretation (Fasting)
        """
        if self.blood_glucose_level < 100:
            return "Normal"
        elif self.blood_glucose_level < 126:
            return "Prediabetes"
        return "High"

    @property
    def bmi_status(self):
        """
        BMI Interpretation
        """
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        return "Obese"

    @property
    def hypertension_status(self):
        if self.hypertension is None:
            return "Not Specified"
        return "Yes" if self.hypertension else "No"

    @property
    def heart_disease_status(self):
        if self.heart_disease is None:
            return "Not Specified"
        return "Yes" if self.heart_disease else "No"

    @property
    def risk_level(self):
        """
        Risk level based on AI confidence score.
        """
        if self.diabetes_confidence is None:
            return "Unknown"

        if self.diabetes_confidence >= 80:
            return "High"

        if self.diabetes_confidence >= 50:
            return "Moderate"

        return "Low"

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"