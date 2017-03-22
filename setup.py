from setuptools import setup

setup(name='operatorinstructions',
      version='0.6.0',
      description='BAE Operator Instruction Management',
      author='Ryan Massoth',
      author_email='rmassoth@baeind.com',
      packages=['operatorinstructions'],
      install_requires=['psycopg2>=2.7',])
