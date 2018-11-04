from setuptools import setup, find_packages

setup(name='PyZatt',
    version='1.0',
    description='Python lib to manage ZKTeco attendance devices',
    author='Alexander Marin',
    author_email='alexanderm2230@gmail.com',
    url='https://github.com/adrobinoga/pyzatt',
    packages=find_packages('lib'),
    package_dir={'':'lib'}
    )
