try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

config = {
    "description": "A game based on the old social hierarchy of Japan",
    "author": "Mason Kuan(pythonmcpi)",
    "url": "https://github.com/pythonmcpi/Japanism",
    "download_url": "https://github.com/pythonmcpi/Japanism",
    "version": "0.1.0",
    "install_requires": [],
    "packages": ["Japanism"],
    "scripts": [],
    "name": "Japanism",
    "python_requires": ">=3.6"
}

setup(**config)
