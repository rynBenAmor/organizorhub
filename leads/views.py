from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import LeadForm, CustomUserCreationForm, LeadCategorForm
from django.views import generic

from django.core.mail import send_mail

from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OroganizorRequiredMixin#accesible to authenticated and is_organizor = True



class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class LandingPageView(generic.TemplateView):
    template_name = 'leads/landing.html'



class LeadListView(LoginRequiredMixin, generic.ListView):
    model_name = Lead
    template_name = 'leads/lead_list.html'
    #queryset constant is only for simple fetching that require no pk or request. or self. we override it
    context_object_name = "leads"
    
    def get_queryset(self):
        user = self.request.user
        #initial queryset based on  role (basically filter for both where a lead has an agent assifned to it)
        if user.is_organizor:#not every organizor is an agent
            queryset = Lead.objects.filter(organization=user.userprofile,agent__isnull=False)# this filters the organizor's leads that belogn only to its organization
        
        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)#cuz every agent has an org
            #show only leads assigned to the respective agent.
            queryset =  Lead.objects.filter(agent__user=user)
        
        return queryset
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)#grab the existing context if any
        user = self.request.user
        if user.is_organizor:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)#to list agentless leads
            context.update({
                "unassigned_leads": queryset
            })
        return context
            
        


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    model_name = Lead
    template_name = 'leads/lead_detail.html'

    def get_queryset(self):
        user = self.request.user
        #initial queryset based on
        if user.is_organizor:
            queryset = Lead.objects.filter(organization=user.userprofile)#not every organizor is an agent
        
        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)#cuz every agent has an org
            #show only leads assigned to the respective agent.
            queryset =  Lead.objects.filter(agent__user=user)
        
        return queryset
            
    
   

class LeadCreateView(OroganizorRequiredMixin, generic.CreateView):
    model = Lead
    template_name = 'leads/lead_create.html'
    form_class = LeadForm

    def form_valid(self, form):
        # Save the form (i.e., save the lead to the database) no matter what
        response = super().form_valid(form)
        from django.contrib import messages  # To show a message if email fails
        # Attempt to send an email, but don't let failure stop the lead from being saved
        try:
            send_mail(
                subject="-----A new lead has been created just now----",
                message="Check it out now on the website",
                from_email="your@boss.com",
                recipient_list=["employee@test.com"]
            )
        except ConnectionRefusedError:
            # Handle the email sending failure gracefully
            messages.error(self.request, 'Could not send the email. Lead saved, but please check email server.')

        # Return the response, ensuring the form is processed and user is redirected
        return response
    

    def get_success_url(self):
        return reverse('leads:list')




class LeadUpdateView(OroganizorRequiredMixin, generic.UpdateView):
    model = Lead
    template_name = 'leads/lead_update.html'
    form_class = LeadForm

    def get_queryset(self):
        user = self.request.user    
          
        return Lead.objects.filter(organization=user.userprofile)# this filters the organizor's leads that belogn only to its organization 
            

    def get_success_url(self):
        return reverse('leads:detail', kwargs={'pk': self.object.pk})
    



class LeadDeleteView(OroganizorRequiredMixin, generic.DeleteView):
    model = Lead
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user        
        return Lead.objects.filter(organization=user.userprofile)# this filters the organizor's leads that belogn only to its organization 
            
    
    def get_success_url(self):
        return reverse ('leads:list')
    



class AssignAgentUpdateView(OroganizorRequiredMixin, generic.UpdateView):
    model = Lead  # Assuming Lead model has an 'agent' ForeignKey field
    fields = ['agent']  # The field you're updating
    template_name = 'leads/lead_assign_agent.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter agents based on the organization of the current user
        form.fields['agent'].queryset = Agent.objects.filter(organization=self.request.user.userprofile)
        return form

    def get_success_url(self) -> str:
        return reverse('leads:list')



#same drill as LeadListView with few changes
class CategoryListView(OroganizorRequiredMixin, generic.ListView):
    
    template_name = 'leads/category_list.html'
    context_object_name = 'categories'
        
    def get_queryset(self):
        user = self.request.user
        
        if user.is_organizor:
            queryset = Category.objects.filter(organization=user.userprofile)
        
        elif user.is_agent:
            queryset = Category.objects.filter(organization=user.agent.organization)          
                    
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_organizor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        
        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)          
        
        context.update({
            'unassigned_lead_count' : queryset.filter(category__isnull=True).count()
             
        })
        return context
    
   


class CategoryDetailView(OroganizorRequiredMixin, generic.DetailView):
    model = Category
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organizor:
            queryset = Category.objects.filter(organization=user.userprofile)
        elif user.is_agent:
            queryset = Category.objects.filter(organization=user.agent.organization)
        
        return queryset
    
    # fk is biderectional 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category = self.get_object()
        
        #leads = Lead.objects.filter(category= self.get_object())# alternatively since we have fk : 
        leads = category.lead_set.all()  
        context.update({
            'leads': leads
        })

        return context




class LeadCategoryUpdateView(OroganizorRequiredMixin, generic.UpdateView):
    model = Category
    template_name = 'leads/category_update.html'
    form_class = LeadCategorForm

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organizor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        
        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            
            queryset =  Lead.objects.filter(agent__user=user)
        
        return queryset
            
    def get_success_url(self):
        return reverse('leads:detail', kwargs={'pk': self.object.pk})




""" 

def landing_page(request):
    return render(request, 'leads/landing.html')

def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'leads/lead_list.html',{'leads': leads,})


def lead_detail(request, pk):
    lead = Lead.objects.get(pk=pk)#.filter returns a query set .get returns 1 object

    return render(request, 'leads/lead_detail.html', {'lead': lead})


def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leads:list')    # After successful submit, return home
    else:#if get request just render empty form
        form = LeadForm()
    
    return render(request, 'leads/lead_create.html', {'form': form})


def lead_update(request, pk):
    lead = Lead.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('leads:list')
    else:
        form = LeadForm(instance=lead)  # Populate the form with existing data
    
    return render(request, 'leads/lead_update.html', {'lead': lead, 'form': form})


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('leads:list')
"""   

