from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='PyZatt',
    version='1.0',
    description='Python lib to manage ZKTeco attendance devices',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Alexander Marin',
    author_email='alexanderm2230@gmail.com',
    url='https://github.com/adrobinoga/pyzatt',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    install_requires=[
          'prettytable', 'colorama',
    ]
    )
