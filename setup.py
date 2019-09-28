from distutils.core import setup


setup(
    name='django-emailuser',
    version='1.1',
    description='simple User model identified by email address',
    packages=['emailuser', 'emailuser.management', 'emailuser.management.commands'],

    author='Andy Duncan',
    author_email='andy@duncaningram.com',
    url='https://github.com/duncaningram/django-emailuser',

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
