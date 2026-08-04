from django import forms
from .models import HealthRecord


class HealthRecordForm(forms.ModelForm):

    pregnancies = forms.IntegerField(
        required=False,
        min_value=0,
        initial=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Number of pregnancies"
            }
        )
    )

    class Meta:

        model = HealthRecord

        exclude = [
            "user",
            "created_at",
            "bmi",
            "diabetes_prediction",
            "diabetes_confidence",
            "diabetic_probability",
            "non_diabetic_probability",
        ]

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
        ]

        widgets = {

            "age": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Age"
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "height": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Height in cm"
                }
            ),

            "weight": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Weight in kg"
                }
            ),

            "blood_pressure": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Systolic BP (Example: 120)"
                }
            ),

            "cholesterol": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cholesterol mg/dL"
                }
            ),

            "glucose": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Glucose mg/dL"
                }
            ),

            "smoking": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "exercise": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "sleep": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Hours of sleep"
                }
            ),

            "alcohol": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "family_history": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }


    def clean(self):

        cleaned_data = super().clean()

        gender = cleaned_data.get("gender")
        pregnancies = cleaned_data.get("pregnancies")

        if gender == "Male":
            cleaned_data["pregnancies"] = 0

        elif gender == "Female" and pregnancies is None:
            self.add_error(
                "pregnancies",
                "Please enter number of pregnancies."
            )

        return cleaned_data


    def clean_age(self):

        age = self.cleaned_data.get("age")

        if age is None:
            raise forms.ValidationError(
                "Age is required."
            )

        if age <= 0:
            raise forms.ValidationError(
                "Enter a valid age."
            )

        return age


    def clean_height(self):

        height = self.cleaned_data.get("height")

        if height is None or height <= 0:
            raise forms.ValidationError(
                "Enter a valid height."
            )

        return height


    def clean_weight(self):

        weight = self.cleaned_data.get("weight")

        if weight is None or weight <= 0:
            raise forms.ValidationError(
                "Enter a valid weight."
            )

        return weight


    def clean_glucose(self):

        glucose = self.cleaned_data.get("glucose")

        if glucose is None or glucose <= 0:
            raise forms.ValidationError(
                "Enter a valid glucose value."
            )

        return glucose


    def clean_blood_pressure(self):

        bp = self.cleaned_data.get("blood_pressure")

        if bp is None:
            raise forms.ValidationError(
                "Blood pressure is required."
            )

        if bp <= 0:
            raise forms.ValidationError(
                "Enter a valid blood pressure value."
            )

        return bp