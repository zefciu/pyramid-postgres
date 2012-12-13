# vim set fileencoding=utf-8
from setuptools import setup

setup(
      name = 'pyramid_postgres',
      version = '0.0.1',
      author = 'Szymon Pyżalski',
      author_email = 'zefciu <szymon@pythonista.net>',
      description =
        'Include this in a pyramid project to get postgres transactions',
      license = 'BSD',
      keywords = 'postgresql psql pg persistence sql relational database',
      
      install_requires = ['pyramid>=1.2', 'psycopg2', 'pyramid-tm'],
      packages = ['pyramid_postgres'],
      classifiers = [
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Topic :: Database :: Front-Ends',
      ]
    
)
