from setuptools import setup, find_packages


setup(
    name='dopc',
    description='Delivery Order Price Calculator service',
    version='0.0.1',
    author='',
    author_email='',
    url='',
    install_requires=['requests==2.31.0', 'StrEnum==0.4.15', 
                      'fastapi==0.115.6','pydantic==2.5.1',
                      'pydantic-extra-types==2.1.0',
                      'pydantic-settings==2.1.0',
                      'pydantic_core==2.14.3',
                      'uvicorn==0.24.0.post1',
                      'httpx==0.25.1',
                      'geopy==2.4.1',
					  'numpy==2.0.1'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
