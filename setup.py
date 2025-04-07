from setuptools import setup, find_packages

setup(
    name='tableascii',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Tariq Muhammed',
    description='A lightweight, simple Python library to create clean ASCII Table.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Tari-dev/tableascii',
    project_urls={
        'Source': 'https://github.com/Tari-dev/tableascii',
        'Bug Tracker': 'https://github.com/Tari-dev/tableascii/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
