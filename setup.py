from distutils.core import setup


setup(
    name='django-emailuser',
    version='1.0',
    description='simple User model identified by email address',
    packages=['emailuser', 'emailuser.management', 'emailuser.management.commands'],

    author='Mark Paschal',
    author_email='markpasc@markpasc.org',
    url='https://github.com/duncaningram/django-emailuser',

    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
