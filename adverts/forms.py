from .models import Advert, Image, ModNote, Category
from django.forms import ModelForm


class AdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = ['category', 'region', 'city', 'title', 'text', 'price']


class AdvertImagesForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class ModNoteForm(ModelForm):
    class Meta:
        model = ModNote
        fields = ['resolution', 'text']

