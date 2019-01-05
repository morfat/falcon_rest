from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='falcon_rest',
      version='0.1',
      description=' REST API development project using Falcon and SqlAlchemy ',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
      ],
      keywords='Falcon REST Python3 SqlAlchemy ',
      url='https://bitbucket.org/morfat/falcon_rest',
      author='Morfat Mosoti',
      author_email='morfatmosoti@gmail.com',
      license='MIT',
      packages=find_packages()
      install_requires=[
         'gunicorn', 'SQLAlchemy', 'falcon'
      ],
      include_package_data=True,
      zip_safe=False)