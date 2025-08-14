from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('agent/', views.agent_dashboard, name='agent_dashboard'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('<int:ticket_id>/ai-response/', views.generate_ai_response, name='generate_ai_response'),
]