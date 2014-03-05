from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from emailuser.models import User


class Command(BaseCommand):

    args = ''
    help = "Clones the project's User models to emailuser.User models"

    def handle(self, *args, **options):
        user_model = get_user_model()
        if user_model is User:
            raise CommandError("The project is already configured to use "
                "emailuser's User model, so we don't know what user data to "
                "convert. Please change the project's AUTH_USER_MODEL "
                "setting to the previous value so we can find the user data "
                "to convert.")

        if user_model.objects.filter(email='').exists():
            raise CommandError("You have existing user models with blank "
                "email addresses. Please fill in email values for all users "
                "before converting them to emailusers.")

        num_users = user_model.objects.count()
        num_users_unique_email = user_model.objects.values('email').distinct().count()
        if num_users_unique_email < num_users:
            raise CommandError("You have existing user models with the same "
                "email address. Please update these conflicting users' email "
                "addresses to uniquely identify them before converting them "
                "to emailusers.")

        emailuser_model_fields = [f.name for f in User._meta.concrete_fields]
        user_data = user_model.objects.values(*emailuser_model_fields)
        emailusers = (User(**d) for d in user_data)
        User.objects.all().delete()
        User.objects.bulk_create(emailusers)

        # TODO: swap our ContentType for the original user_model's to preserve generic foreign key references?

        self.stdout.write("Converted {} {}.{} models into emailuser.User models".format(
            len(user_data), user_model.__module__, user_model.__name__))
