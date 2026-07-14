from django import forms
from .models import HealthRecord


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        exclude = ["user", "created_at"]
        fields = {
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "height": forms.NumberInput(attrs={"class": "form-control"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),
            # "bmi": forms.NumberInput(attrs={"class": "form-control"}),
            "blood_pressure": forms.TextInput(attrs={"class": "form-control"}),
            "cholesterol": forms.NumberInput(attrs={"class": "form-control"}),
            "glucose": forms.NumberInput(attrs={"class": "form-control"}),
            "smoking": forms.Select(attrs={"class": "form-select"}),
            "exercise": forms.Select(attrs={"class": "form-select"}),
            "sleep": forms.NumberInput(attrs={"class": "form-control"}),
            "alcohol": forms.Select(attrs={"class": "form-select"}),
            "family_history": forms.Select(attrs={"class": "form-select"}),

        }