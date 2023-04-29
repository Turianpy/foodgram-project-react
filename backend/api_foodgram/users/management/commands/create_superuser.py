from django.core.management.base import BaseCommand

from users.models import User, UserProfile


class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **options):
        username = input('Enter username:')
        password = input('Enter password:')
        user = User.objects.create_superuser(
            username=username,
            password=password,
            email=f'{username}@foodgram.com'
        )
        UserProfile.objects.create(user=user)
        self.stdout.write(
            self.style.SUCCESS(f'Superuser created. Email: {user.email}')
        )
