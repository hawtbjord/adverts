from django import forms
from accounts.models import CustomUser
from adverts.models import Category, Region, City


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'groups')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'patronymic', 'phone_number', 'calls_time', 'groups', 'is_active'
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent', 'slug')


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ('name',)


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name', 'region')
