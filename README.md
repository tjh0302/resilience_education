# Resilience Education - chatbot for helping formerly incarcerated job-seekers navigate VA legal restrictions.

Brief description of the project.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

Step 1: Download the LLM using Ollama

Step 2: Clone repo (this is needed to retrain the model but not to simply use the model)

If you do not have a personal access token yet here are the instruction to create Tokens(classic)
Then you can clone the repository
     git clone https://<your_access_token>@github.com/hparten/resilience_education.git

Step 3: Import zipped "embeddings" folder

These embedings were too large to include in the github repo so please remeber to add it to your local directory.

Step 4: Install package

    pip install <our package>
Usage
Example of how the package works
   import <our package>
   

├── LICENSE
├── README.md
├── makefile
├── pkg_tree.md
├── rag_dev
│   ├── generate_embeddings.ipynb
│   ├── generate_embeddings.py
│   ├── rag_executable.ipynb
│   ├── setup_rag.ipynb
│   └── test_rag.ipynb
├── rag_executable.py
├── ragas_results
│   ├── ragas_results.csv
│   ├── ragas_results2.csv
│   ├── test.csv
│   └── test2.csv
├── ragsilience
│   ├── __init__.py
│   └── setup_rag.py
├── requirements-dev.txt
├── requirements.txt
├── setup.py
└── tests
    └── test_rag.py
