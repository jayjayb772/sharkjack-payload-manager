from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'sharkjackpayloadmanager',
    version = '0.0.1',
    author = 'June bender',
    author_email = 'jay@j-bender-portfolio.me',
    license = 'MIT',
    description = 'Easily switch payloads on a sharkjack with this cli tool',
    long_description = 'Easily switch payloads on a sharkjack with this cli tool',
    long_description_content_type = "text/markdown",
    url = '<github url where the tool code will remain>',
    py_modules = ['payload_manager', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        listpayloads=payload_manager:list
        setpayload=payload_manager:set
        getpayload=payload_manager:get
    '''
)
