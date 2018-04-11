import os

from setuptools import setup


setup(name='fiubar',
      version='2.0.0',
      zip_safe=False,
      include_package_data=True,
      description='Administrador de materias para FIUBA',
      long_description=open(os.path.join(os.path.dirname(__file__),
                                         'README.md')).read(),
      author='Maru Berezin',
      url='https://github.com/maru/fiubar/',
      packages=['fiubar', 'fiubar.tests'],
      test_suite='fiubar.runtests.run_tests',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Framework :: Django :: 2.0',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3'],
      install_requires=[
          'Django>=2',
      ],
)
