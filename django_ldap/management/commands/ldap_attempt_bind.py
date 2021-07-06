from django.core.management.base import BaseCommand
from django_ldap.ldap import ldap_connection


class Command(BaseCommand):
    help = "Attempts to bind to LDAP server"

    # Example: python manage.py ldap_attempt_bind

    def handle(self, *args, **options):
        with ldap_connection() as conn:
            print(conn)
