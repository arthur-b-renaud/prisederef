from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'List all recruiter users'

    def handle(self, *args, **options):
        users = User.objects.all().order_by('date_joined')
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found in the system.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {users.count()} user(s):'))
        self.stdout.write('')
        
        for user in users:
            full_name = f"{user.first_name} {user.last_name}".strip() or user.username
            self.stdout.write(f'• {full_name} ({user.email})')
            self.stdout.write(f'  Username: {user.username}')
            self.stdout.write(f'  Created: {user.date_joined.strftime("%Y-%m-%d %H:%M:%S")}')
            self.stdout.write(f'  Last login: {user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "Never"}')
            self.stdout.write('')
