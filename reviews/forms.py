from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    accuracy = forms.IntegerField(
        max_value=5,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input",
            }
        ),
    )
    communication = forms.IntegerField(
        max_value=5,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input",
            }
        ),
    )
    cleanliness = forms.IntegerField(
        max_value=5,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input",
            }
        ),
    )
    location = forms.IntegerField(
        max_value=5,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input",
            }
        ),
    )
    check_in = forms.IntegerField(
        max_value=5,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input",
            }
        ),
    )
    value = forms.IntegerField(
        max_value=5,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input",
            }
        ),
    )

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )

    def save(self):
        review = super().save(commit=False)
        return review
