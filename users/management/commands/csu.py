from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='burykh_2000@mail.com',
            first_name='admin',
            last_name='skypro',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password('simba2106')
        user.save()