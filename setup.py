from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Zerodha Login Automation - Selenium Based'
with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="zlogin",
    version=VERSION,
    author="Prabhat Rastogi",
    author_email="prabhatrastogik@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license="MIT",
    install_requires=['boto3', 'undetected_chromedriver',
                      'selenium'],  # add any additional packages that
    keywords=['selenium login', 'zerodha', 'automate zerodha'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
