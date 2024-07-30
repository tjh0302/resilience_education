from setuptools import setup, find_packages

# Read the contents of requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

# Parse the requirements
install_requires = parse_requirements('requirements.txt')

setup(
    name="RAGsilience",
    version="0.1.0", 
    description="A chatbot for helping formerly incarcerated job-seekers navigate VA legal restrictions.",
    author="Hallie Parten, Tyler Hinnendael, Christa Lesher",
    author_email="hallieparten@gmail.com",  
    url="https://github.com/hparten/resilience_education",  
    packages=find_packages(), 
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'my-script=ragsilience:setup_rag',  # Replace with your module and function
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10.9',  # Adjust based on your project's Python version requirements
)
