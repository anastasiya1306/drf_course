from django.core.management import BaseCommand

from users.models import User, UserRoles


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='vinston768@gmail.com',
            first_name='skypro',
            last_name='test',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MODERATOR,
        )
        user.set_password('abc123def456')
        user.save()
