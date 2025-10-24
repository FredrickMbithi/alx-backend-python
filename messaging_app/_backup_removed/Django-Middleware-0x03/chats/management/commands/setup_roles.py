# chats/management/commands/setup_roles.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from chats.models import Conversation, Message

class Command(BaseCommand):
    help = 'Setup user roles and permissions for testing middleware'
    
    def handle(self, *args, **options):
        # Create groups
        admin_group, created = Group.objects.get_or_create(name='admin')
        moderator_group, created = Group.objects.get_or_create(name='moderator')
        
        self.stdout.write(
            self.style.SUCCESS(f'Created groups: admin, moderator')
        )
        
        # Create test users
        users_data = [
            {'username': 'admin_user', 'email': 'admin@test.com', 'password': 'admin123', 'group': 'admin'},
            {'username': 'mod_user', 'email': 'mod@test.com', 'password': 'mod123', 'group': 'moderator'},
            {'username': 'regular_user', 'email': 'user@test.com', 'password': 'user123', 'group': None},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['username'].replace('_', ' ').title(),
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                
                # Add user to group
                if user_data['group'] == 'admin':
                    admin_group.user_set.add(user)
                    user.is_staff = True
                    user.save()
                elif user_data['group'] == 'moderator':
                    moderator_group.user_set.add(user)
                
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.username} with role: {user_data["group"] or "regular"}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user.username}')
                )
        
        # Add permissions to groups
        conversation_ct = ContentType.objects.get_for_model(Conversation)
        message_ct = ContentType.objects.get_for_model(Message)
        
        # Admin permissions (all)
        all_conversation_perms = Permission.objects.filter(content_type=conversation_ct)
        all_message_perms = Permission.objects.filter(content_type=message_ct)
        
        admin_group.permissions.set(list(all_conversation_perms) + list(all_message_perms))
        
        # Moderator permissions (limited)
        moderator_perms = Permission.objects.filter(
            content_type__in=[conversation_ct, message_ct],
            codename__in=['view_conversation', 'view_message', 'delete_message']
        )
        moderator_group.permissions.set(moderator_perms)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up roles and permissions!')
        )
        self.stdout.write(
            self.style.SUCCESS('Test users created:')
        )
        self.stdout.write('  - admin_user (password: admin123) - Admin role')
        self.stdout.write('  - mod_user (password: mod123) - Moderator role') 
        self.stdout.write('  - regular_user (password: user123) - Regular user')