from setuptools import setup, find_packages

setup(
    name='django-marionette',
    version='0.0.2',
    description='A simple RPC library for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/django-marionette',
    keywords=['django', 'json', 'rpc'],
    packages = find_packages(exclude=('tests*',)),
    zip_safe=False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    requires = [
        'Django (>=1.6)',
    ],
    install_requires = [
        'Django>=1.6',
    ],
)
