from pathlib import Path
from setuptools import setup, find_packages

long_description = Path('README.md').read_text()

setup(
    name='saidai-ical-generator',
    version='0.1.0',
    author='kimotu4632uz',
    description='ics generator from saidai-kyoumu site',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kimotu4632uz/saidai_ical_generator',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows'
    ],
    entry_points = {
        'console_scripts': ['saidai-ical-generator = src.main:main']
    },
    python_requires='>=3.7',
)
