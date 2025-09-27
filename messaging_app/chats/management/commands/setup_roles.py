# chats/management/commands/setup_roles.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Setup user roles and permissions for testing middleware'
    
    def handle(self, *args, **options):
        # Create groups
        admin_group, created = Group.objects.get_or_create(name='admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Created admin group'))
        
        moderator_group, created = Group.objects.get_or_create(name='moderator')
        if created:
            self.stdout.write(self.style.SUCCESS('Created moderator group'))
        
        # Create test users
        users_data = [
            {
                'username': 'admin_user', 
                'email': 'admin@test.com', 
                'password': 'admin123', 
                'group': 'admin',
                'is_staff': True
            },
            {
                'username': 'mod_user', 
                'email': 'mod@test.com', 
                'password': 'mod123', 
                'group': 'moderator',
                'is_staff': False
            },
            {
                'username': 'regular_user', 
                'email': 'user@test.com', 
                'password': 'user123', 
                'group': None,
                'is_staff': False
            },
        ]
        
        for user_data in users_data:
            try:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['username'].replace('_', ' ').title(),
                    is_staff=user_data['is_staff']
                )
                
                # Add user to group
                if user_data['group'] == 'admin':
                    admin_group.user_set.add(user)
                elif user_data['group'] == 'moderator':
                    moderator_group.user_set.add(user)
                
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.username} with role: {user_data["group"] or "regular"}')
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user_data["username"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\nTest users created with passwords:')
        )
        self.stdout.write('  - admin_user (password: admin123) - Admin role')
        self.stdout.write('  - mod_user (password: mod123) - Moderator role') 
        self.stdout.write('  - regular_user (password: user123) - Regular user')
        self.stdout.write('\nYou can now test the middleware with different user roles!')