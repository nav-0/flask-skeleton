from setuptools import setup, find_packages

API_VERSION = 'v1'

setup(
  name='i_go_by',
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
      'i_go_by_api = i_go_by.__main__:main_api',
      'i_go_by_client = i_go_by.__main__:main_client',
      'i_go_by_cli = i_go_by.__main__:main_cli',
      'i_go_by_something_else_i_do = i_go_by.__main__:something_else_i_do',
    ]
  },
)
  
