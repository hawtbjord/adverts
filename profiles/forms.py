from django import forms
from accounts.models import CustomUser


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
