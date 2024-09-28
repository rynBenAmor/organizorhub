from . import views
from django.urls import path

app_name = 'leads'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),

    path('leads/', views.LeadListView.as_view(), name='list'),
    path('leads/create/', views.LeadCreateView.as_view(), name='create'),
    path('leads/detail/<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('leads/update/<int:pk>/', views.LeadUpdateView.as_view(), name='update'),
    path('leads/delete/<int:pk>/', views.LeadDeleteView.as_view(), name='delete'),
    path('leads/assign_agent/<int:pk>/', views.AssignAgentUpdateView.as_view(), name='assign'),

    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category_detail/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
