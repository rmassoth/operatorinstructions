from setuptools import setup

setup(name='operatorinstructions',
      version='1.2.0',
      description='BAE Operator Instruction Management',
      author='Ryan Massoth',
      author_email='rmassoth@baeind.com',
      packages=['operatorinstructions'],
      install_requires=['psycopg2>=2.7'],
      entry_points={
        'console_scripts':[
            'operatorinstructions = operatorinstructions.__main__:main'
        ]
      },
      )
