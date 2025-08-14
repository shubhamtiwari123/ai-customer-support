from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('agent/', views.agent_dashboard, name='agent_dashboard'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ai-response/<int:ticket_id>/', views.generate_ai_response, name='generate_ai_response'),
]