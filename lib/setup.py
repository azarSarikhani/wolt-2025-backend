from setuptools import setup, find_packages


setup(
    name='dopc',
    description='Delivery Order Price Calculator service',
    version='0.0.1',
    author='',
    author_email='',
    url='',
    install_requires=['requests==2.31.0', 'StrEnum==0.4.15'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
