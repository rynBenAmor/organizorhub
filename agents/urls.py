
from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('', views.AgentListView.as_view(), name='list'),
    path('create/', views.AgentCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', views.AgentDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.AgentUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.AgentDeleteView.as_view(), name='delete'),
]