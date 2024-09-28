#from django.contrib.auth.mixins import LoginRequiredMixin : i made a custom mixin that overrides this

from .mixins import OroganizorRequiredMixin #custom mixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from leads.models import Agent
from .forms import AgentForm

from django.core.mail import send_mail
from django.contrib import messages






class AgentListView(OroganizorRequiredMixin, generic.ListView):
    model = Agent
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):        
        #From User, you can access the UserProfile using .userprofile.
        myrequest_organization = self.request.user.userprofile
        return Agent.objects.filter(organization=myrequest_organization)
    


class AgentCreateView(generic.CreateView):
    model = Agent
    template_name = 'agents/agent_create.html'
    form_class = AgentForm


    #basically it creates intances of  a User > automatically UserProfile (dj signals) > and with those info manuall Agent (in the view)
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save(commit=False)  # Save the form but don't commit to the database yet
        user.is_agent = True
        user.is_organizor = False
        user.set_password("password2strongXD")
        user.save()

        # Create an Agent linked to the User and Organization manually with the newly made User instance 
        Agent.objects.create(user=user, organization=self.request.user.userprofile)
        
        # Attempt to send an email notification to the new agent
        try:
            send_mail(
                subject="---- A new *job* assignment ---",
                message="You have been picked to be the agent, please login with the new credentials",
                from_email="your-boss@test.com",
                recipient_list=[user.email],  # Use the agent's email
            )
        except ConnectionRefusedError:
            messages.error(self.request, 'Could not send the email. Agent saved, but please check email server.')

        return super().form_valid(form)  # Call the parent method to finalize the form submission    

    def get_success_url(self) -> str:
        return reverse("agents:list")  # Redirects to the agent list after creation



class AgentDetailView(OroganizorRequiredMixin, generic.DetailView):
    model = Agent
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'
    queryset = Agent.objects.all()



class AgentUpdateView(OroganizorRequiredMixin, generic.UpdateView):
    model = Agent
    template_name = 'agents/agent_update.html'
    form_class = AgentForm

    def get_success_url(self):
        return reverse('agents:detail', kwargs={'pk': self.object.pk})



class AgentDeleteView(generic.DeleteView):
    model = Agent
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'

    def get_success_url(self) -> str:
        return reverse('agents:list')