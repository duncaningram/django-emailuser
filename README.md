# django-emailuser #

django-emailuser provides an `User` model for use with `django.contrib.auth` that is identified by email address. The `emailuser.User` model also omits the first & last name fields altogether. Otherwise the provided `User` works just like the `contrib.auth` `User` model, using the extension mechanisms available in Django 1.5+.
