# django-emailuser #

django-emailuser provides a `User` model for use with `django.contrib.auth` that is identified by email address. The `emailuser.User` model also omits the first & last name fields altogether. Otherwise the provided `User` works just like the `contrib.auth` `User` model, using the extension mechanisms available in Django 2.2+.


## Install ##

Install django-emailuser into your Python environment as you would any other Python package.

    $ python setup.py install


## Convert an existing project ##

If you have an existing project you want to convert to use django-emailuser, you can in several easy steps.

1. Add the `emailuser` app to your project.

        # settings.py

        INSTALLED_APPS = (
            'django.contrib.auth',
            'emailuser',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            # ...
        )

2. Run `migrate emailuser` to create the `emailuser.User` tables.


        (env) $ python manage.py migrate emailuser
        Operations to perform:
          Apply all migrations: emailuser
        Running migrations:
          Applying emailuser.0001_initial... OK
        ...
        (env) $

3. Run the `converttoemailuser` management command to convert your existing user model records to `emailuser.User` records.

        (env) $ python manage.py converttoemailuser
        Converted 2 django.contrib.auth.models.User models into emailuser.User models
        (env) $

   If you have user records with blank or duplicate email addresses, the conversion will abort with an error to that effect. Change your existing user models (using the shell or web admin) to uniquely identify each user with a valid email address before converting.

4. Set the `AUTH_USER_MODEL` setting to use the `emailuser.User` model.

        # settings.py

        AUTH_USER_MODEL = 'emailuser.User'

5. If your project contains models that use [generic foreign keys][] to the user model, update those records to use the `emailuser.User` model's content type instead.

6. If you were using Django's `auth.User` model, run `migrate emailuser` to remove the stale [content type][] model record for the swapped-out user model. (As with other inactive models, this won't remove the `auth_user` or other previous user model's table, only the `django_content_type` record referring to that model.)

        (env) $ python manage.py migrate emailuser
        Syncing...
        Creating tables ...
        The following content types are stale and need to be deleted:

            auth | user

        Any objects related to these content types by a foreign key will also
        be deleted. Are you sure you want to delete these content types?
        If you're unsure, answer 'no'.

            Type 'yes' to continue, or 'no' to cancel: yes
        Installing custom SQL ...
        ...
        (env) $

[generic foreign keys]: https://docs.djangoproject.com/en/2.2/ref/contrib/contenttypes/#django.contrib.contenttypes.fields.GenericForeignKey
[content type]: https://docs.djangoproject.com/en/2.2/ref/contrib/contenttypes/


## Use in a new project ##

For a new Django project with no user records, before you `syncdb`, add the `emailuser` app to your `INSTALLED_APPS` setting and set `AUTH_USER_MODEL` to `emailuser.User`:

    INSTALLED_APPS = (
        'django.contrib.auth',
        'emailuser',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        # ...
    )

    AUTH_USER_MODEL = 'emailuser.User'

Then use `makemigrations`, `migrate emailuser`, and `migrate` to create the database tables and continue as normal.
