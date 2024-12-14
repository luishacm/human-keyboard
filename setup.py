from setuptools import setup, find_packages

setup(
    name='human-keyboard',
    version='0.1.0',
    author='@luishacm',
    author_email='noemail',
    description='Simulates human typing behavior with realistic timing and errors.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/luishacm/human-keyboard',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'keyboard',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)