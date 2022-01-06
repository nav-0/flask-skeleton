from setuptools import setup, find_packages

API_VERSION = 'v1'

setup(
  name='en_passant',
  version=API_VERSION,
  description='we all have a part to play',
  author='nav-0',
  author_email='whatyoulookin@wallace.com',
  packages=find_packages(),
  install_requires=[
    'flask==1.1.2', # i could be another version
    'flask-pymongo',
    'flask-restful',
    'pymongo',
    'pandas',
    'python-dotenv',
    'requests',
    'simplejson',
    # i might have other needs
  ],
  extras_require={
    'dev': [
      'pylint',
      'pytest',
      'pytest-asyncio',
    ],
  },
  entry_points={
    'console_scripts': [
      'en_passant_api = en_passant.__main__:main_api',
      'en_passant_client = en_passant.__main__:main_client',
      'en_passant_cli = en_passant.__main__:main_cli',
      'en_passant_something_else_i_do = en_passant.__main__:something_else_i_do',
    ]
  },
)
  
