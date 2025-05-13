from setuptools import setup, find_packages


# Function to read requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name='Phenomix',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
    'console_scripts': [
        'phenomix-run=main:main',  
    ],
    },
    author='Princia Fernandes, Ashith A V',
    author_email='princiafer2002@gmail.com, ashithavgowda@gmail.com',
    description='Integrating Graph Databases and Vector Embeddings for Advanced Phenotype Search using llms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/PrinciaFernandes/Phenomix',
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

