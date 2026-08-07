from django import forms
from .models import HealthRecord


class HealthRecordForm(forms.ModelForm):

    YES_NO_CHOICES = [
        ("", "-- Select --"),
        ("True", "Yes"),
        ("False", "No"),
    ]

    hypertension = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == "True",
        empty_value=None,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    heart_disease = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == "True",
        empty_value=None,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:

        model = HealthRecord

        exclude = [
            "user",
            "created_at",
            "diabetes_prediction",
            "diabetes_confidence",
            "diabetic_probability",
            "non_diabetic_probability",
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


            "race": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),



            "bmi": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "BMI"
                }
            ),


            "hbA1c_level": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "HbA1c Level"
                }
            ),


            "blood_glucose_level": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Blood Glucose Level"
                }
            ),


            "smoking_history": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

        }



    # -----------------------------------
    # Add -- Select -- placeholder
    # -----------------------------------

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        dropdown_fields = [
            "gender",
            "race",
            "hypertension",
            "heart_disease",
            "smoking_history",
        ]


        for field_name in dropdown_fields:

            self.fields[field_name].choices = [
                ("", "-- Select --")
            ] + list(
                self.fields[field_name].choices
            )


            self.fields[field_name].required = True



    # -----------------------------------
    # Age validation
    # -----------------------------------

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



    # -----------------------------------
    # BMI validation
    # -----------------------------------

    def clean_bmi(self):

        bmi = self.cleaned_data.get("bmi")


        if bmi is None:

            raise forms.ValidationError(
                "BMI is required."
            )


        if bmi <= 0:

            raise forms.ValidationError(
                "Enter a valid BMI value."
            )


        return bmi



    # -----------------------------------
    # HbA1c validation
    # -----------------------------------

    def clean_hbA1c_level(self):

        value = self.cleaned_data.get(
            "hbA1c_level"
        )


        if value is None:

            raise forms.ValidationError(
                "HbA1c level is required."
            )


        if value <= 0:

            raise forms.ValidationError(
                "Enter a valid HbA1c value."
            )


        return value



    # -----------------------------------
    # Blood glucose validation
    # -----------------------------------

    def clean_blood_glucose_level(self):

        value = self.cleaned_data.get(
            "blood_glucose_level"
        )


        if value is None:

            raise forms.ValidationError(
                "Blood glucose is required."
            )


        if value <= 0:

            raise forms.ValidationError(
                "Enter a valid glucose value."
            )


        return value



    # -----------------------------------
    # Dropdown validation
    # -----------------------------------

    def clean(self):

        cleaned_data = super().clean()


        select_fields = [
            "gender",
            "race",
            "hypertension",
            "heart_disease",
            "smoking_history",
        ]


        for field in select_fields:

            value = cleaned_data.get(field)


            # IMPORTANT:
            # Do not use "if not value"
            # because 0 = No is valid

            if value is None or value == "":

                self.add_error(
                    field,
                    "Please select an option."
                )


        return cleaned_data