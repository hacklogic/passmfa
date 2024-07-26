from django import forms
from .models import AppCredentials

class AppCredentialsForm(forms.ModelForm):
    class Meta:
        model = AppCredentials
        fields = ['app_name', 'app_url', 'app_username', 'app_password', 'app_two_fa','app_note']
        #widgets = {
        #    'app_password': forms.PasswordInput(),
        #    'app_two_fa': forms.PasswordInput(),
        #}

class UploadFileForm(forms.Form):
    file = forms.FileField()

class ShareCredentialsForm(forms.ModelForm):
    class Meta:
        model = AppCredentials
        fields = ['shared_with_users', 'shared_with_groups']
        #widgets = {
        #    'shared_with_users': forms.CheckboxSelectMultiple(),
        #    'shared_with_groups': forms.CheckboxSelectMultiple(),
        #}