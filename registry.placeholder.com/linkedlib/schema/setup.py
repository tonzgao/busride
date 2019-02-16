from setuptools import setup

requires = [
  'psycopg2',
  'sqlalchemy',
  'transaction',
  'zope.sqlalchemy',
]

setup(
  name="schema",
  version="1.0",
  author="busride",
  author_email="",
  description="",
  license="",
  keywords="",
  url="https://www.example.com.com",
  packages=['schema'],
  long_description='busride database connection',
  classifiers=[
    "Topic :: Utilities"
  ],
  install_requires=requires
)

