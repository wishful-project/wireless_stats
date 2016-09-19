from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='wishful_wifi_stats',
    version='0.1.0',
    packages=find_packages(),
    url='http://www.wishful-project.eu/software',
    license='',
    author='Anatolij Zubow',
    author_email='zubow@tu-berlin.de',
    description='WiSHFUL WiFi stats module',
    long_description='Implementation of Wifi stats',
    keywords='wireless control',
    install_requires=[]
)
