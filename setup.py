from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/ngocjr7/geneticpython/issues',
    'Documentation': 'https://github.com/ngocjr7/geneticpython/blob/master/README.md',
    'Source Code': 'https://github.com/ngocjr7/geneticpython'
}

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(name='geneticpython',
      description='A simple and friendly Python framework for genetic-based algorithms',
      author='Ngoc Bui',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author_email='ngocjr7@gmail.com',
      version='0.0.1', 
      packages=find_packages(),
      install_requires=install_requires,
      python_requires='>=3.6')
