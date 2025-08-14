from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Create demo users and groups'
    
    def handle(self, *args, **options):
        # Create groups
        customer_group, created = Group.objects.get_or_create(name='Customers')
        agent_group, created = Group.objects.get_or_create(name='Support_Agents')
        
        self.stdout.write('Groups created/verified')
        
        # Create customer user
        if not User.objects.filter(username='customer2').exists():
            customer_user = User.objects.create_user(
                username='customer1',  
                password='password123',
                email='customer@example.com'
            )
            customer_user.groups.add(customer_group)
            self.stdout.write(
                self.style.SUCCESS('Created customer1 user')
            )
        else:
            self.stdout.write('Customer1 user already exists')
        
        # Create agent 
        if not User.objects.filter(username='agent2').exists():
            agent_user = User.objects.create_user(
                username='agent1',  
                password='password123',
                email='agent@example.com'
            )
            agent_user.groups.add(agent_group)
            agent_user.is_staff = True
            agent_user.save()
            self.stdout.write(
                self.style.SUCCESS('Created agent1 user')
            )
        else:
            self.stdout.write('Agent1 user already exists')
        
        self.stdout.write(
            self.style.SUCCESS('Demo users setup complete!')
        )