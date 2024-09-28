from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



User = get_user_model()#our authenticated model


class AgentForm(forms.ModelForm):
    class Meta:
        model = User#this will have implications on the leads.models.User model
        fields = ('username','first_name', 'last_name', 'email')#basically it creates intances of  a User > automatically UserProfile (dj signals) > and with those info manuall Agent (in the view)
        