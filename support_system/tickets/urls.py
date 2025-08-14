from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('agent/', views.agent_dashboard, name='agent_dashboard'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ai-response/<int:ticket_id>/', views.generate_ai_response, name='generate_ai_response'),
]