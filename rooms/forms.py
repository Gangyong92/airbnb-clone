from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = (
            "caption",
            "file",
        )
        widgets = {
            "caption": forms.TextInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "file": forms.FileInput(
                attrs={
                    "class": "form-input",
                }
            ),
        }

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "guests": forms.NumberInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "beds": forms.NumberInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "bedrooms": forms.NumberInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "baths": forms.NumberInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "check_in": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "HH:MM:SS",
                }
            ),
            "check_out": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "HH:MM:SS",
                }
            ),
        }

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
