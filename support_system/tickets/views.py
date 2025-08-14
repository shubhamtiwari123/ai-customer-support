from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from .models import Ticket, Reply
from .forms import TicketForm, ReplyForm
from .services.ai_service import GeminiAIService
import json

@login_required
def dashboard(request):
    """Main dashboard that redirects based on authentication and user role"""
    # Check if user is an agent (staff or in agent group)
    if request.user.is_staff or request.user.groups.filter(name='Agent').exists():
        return redirect('agent_dashboard')
    else:
        return redirect('customer_dashboard')

@login_required
def customer_dashboard(request):
    """Customer dashboard showing their tickets"""
    # Ensure only customers can access this
    if request.user.is_staff or request.user.groups.filter(name='Agent').exists():
        return redirect('agent_dashboard')
    
    tickets = Ticket.objects.filter(customer=request.user)
    return render(request, 'tickets/customer_dashboard.html', {'tickets': tickets})

@login_required
def agent_dashboard(request):
    """Agent dashboard showing pending tickets"""
    if not (request.user.is_staff or request.user.groups.filter(name='Agent').exists()):
        return redirect('customer_dashboard')
    
    tickets = Ticket.objects.filter(status='pending')
    return render(request, 'tickets/agent_dashboard.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    """Create a new support ticket (customers only)"""
    # Ensure only customers can create tickets
    if request.user.is_staff or request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Agents cannot create tickets.")
        return redirect('agent_dashboard')
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.save()
            messages.success(request, "Ticket created successfully!")
            return redirect('customer_dashboard')
    else:
        form = TicketForm()
    
    return render(request, 'tickets/create_ticket.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    """View and respond to a specific ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check permissions
    is_agent = request.user.is_staff or request.user.groups.filter(name='Agent').exists()
    if not is_agent and ticket.customer != request.user:
        messages.error(request, "You don't have permission to view this ticket.")
        return redirect('dashboard')
    
    replies = ticket.replies.all()
    
    if request.method == 'POST' and is_agent:
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.agent = request.user
            reply.save()
            
            # Update ticket status
            ticket.status = 'replied'
            ticket.save()
            
            messages.success(request, "Reply sent successfully!")
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = ReplyForm()
    
    context = {
        'ticket': ticket,
        'replies': replies,
        'form': form,
        'is_agent': is_agent
    }
    return render(request, 'tickets/ticket_detail.html', context)

@login_required
@require_POST
def generate_ai_response(request, ticket_id):
    """Generate AI response for a ticket (agents only)"""
    # Check if user is an agent
    if not (request.user.is_staff or request.user.groups.filter(name='Agent').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    ai_service = GeminiAIService()
    response = ai_service.generate_response(
        ticket.subject, 
        ticket.message, 
        ticket.category
    )
    
    return JsonResponse({'response': response})

def custom_login(request):
    """Custom login view with proper error handling"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')

def custom_logout(request):
    """Custom logout view that accepts both GET and POST"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')