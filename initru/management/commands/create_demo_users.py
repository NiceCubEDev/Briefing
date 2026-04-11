from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create one admin user and one regular demo user."

    def handle(self, *args, **options):
        User = get_user_model()
        users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password": "admin12345",
                "first_name": "Admin",
                "last_name": "Briefing",
                "patronymic": "Demo",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "user",
                "email": "user@example.com",
                "password": "user12345",
                "first_name": "User",
                "last_name": "Briefing",
                "patronymic": "Demo",
                "is_staff": False,
                "is_superuser": False,
            },
        ]

        for user_data in users:
            password = user_data.pop("password")
            username = user_data["username"]
            user, created = User.objects.get_or_create(
                username=username,
                defaults=user_data,
            )

            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))
                continue

            changed = False
            for field, value in user_data.items():
                if getattr(user, field) != value:
                    setattr(user, field, value)
                    changed = True

            if not user.has_usable_password():
                user.set_password(password)
                changed = True

            if changed:
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Updated user: {username}"))
            else:
                self.stdout.write(f"User already exists: {username}")
