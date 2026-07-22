from django import forms
from .models import HealthRecord


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord

        exclude = ["user", "created_at", "bmi"]

        fields = [
            "age",
            "gender",
            "height",
            "weight",
            "blood_pressure",
            "cholesterol",
            "glucose",
            "smoking",
            "exercise",
            "sleep",
            "alcohol",
            "family_history",
            "pregnancies",
            # "skin_thickness",
            # "insulin",
            # "diabetes_pedigree_function",
        ]

        widgets = {
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),

            "height": forms.NumberInput(attrs={"class": "form-control"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),

            "blood_pressure": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 120/80"
                }
            ),

            "cholesterol": forms.NumberInput(attrs={"class": "form-control"}),
            "glucose": forms.NumberInput(attrs={"class": "form-control"}),

            "smoking": forms.Select(attrs={"class": "form-select"}),
            "exercise": forms.Select(attrs={"class": "form-select"}),

            "sleep": forms.NumberInput(attrs={"class": "form-control"}),

            "alcohol": forms.Select(attrs={"class": "form-select"}),
            "family_history": forms.Select(attrs={"class": "form-select"}),

            "pregnancies": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Number of pregnancies"}),
            "skin_thickness": forms.NumberInput(attrs={"class": "form-control"}),
            "insulin": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Insulin level such as: 100 mg/dl"}),
            "diabetes_pedigree_function": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }