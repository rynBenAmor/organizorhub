from .models import Lead, Agent
from django.contrib.auth import get_user_model
from django import forms

from django.contrib.auth.forms import UserCreationForm


# Get the current active user model dynamically for our login form
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User  # Use the dynamically fetched user model
        fields = ('username','email')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Ensuring the email is unique (similar to unique=True)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        
        return email


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('first_name', 'last_name', 'age', 'agent', 'organization')



        

"""
class AssignAgentForm(forms.Form):    
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")        
        agents = Agent.objects.filter(organization=request.user.userprofile)
        
        super().__init__(*args, **kwargs)#initialize the form

        self.fields["agent"].queryset = agents

"""

"""
removed because in this context we can use ModelForms
class LeadForm(forms.Form):
    first_name = forms.CharField( )
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=18 ,required=False)
"""
