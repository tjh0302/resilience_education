# RAGsilience
A chatbot for helping formerly incarcerated job-seekers navigate VA legal restrictions.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Repository Structure](#structure)
- [Development](#development)
- [License](#license)

## Installation

### Step 1: Download the LLM using Ollama

#### CLI - 

#### GUI - 

### Step 2: Download zipped "embeddings" folder

Download the zipped embeddings folder your email. Save the folder locally and save the pathname for configuring the package.

### Step 3: Install package

```bash
pip install git+https://github.com/hparten/resilience_education.git
```

## Usage

### Example 1 - Single Query

```python
from ragsilience.setup_rag import create_rag_session

# Create a session
session_id = "<session_id>"
embeddings_path = "<local_path_to_embeddings_folder"

rag_session = create_rag_session(session_id, embeddings_path)
     
rag_session.ask()
```

### Example 2 - Query Stream
```python

while True:
     response = rag_session.ask()

```

## Structure

```bash
├── LICENSE
├── README.md
├── makefile
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
```

## Development

1. **Fork the Repository**
   - Click the "Fork" button at the top right of this repository to create a personal copy.

2. **Clone Your Fork**
   - Clone your forked repository to your local machine:
     ```bash
     git clone https://github.com/your-username/resilience_education.git
     ```

3. **Create a New Branch**
   - Create a new branch for your changes:
     ```bash
     git checkout -b feature/your-feature-name
     ```
4. **Set up Development Environment**
   - run the following command to create a development environment in JupyterLab
     ```bash
     make jupyterlab
     ```

4. **Make Your Changes**
   - Make changes or add features as needed. Be sure to write clear and concise commit messages.

5. **Test Your Changes**
   - Run the tests to ensure your changes don’t break anything:
     ```bash
     make test
     ```

6. **Commit & Push Your Changes**
   - Push your changes to your fork:
     ```bash
     git add .
     git commit -m "Describe your changes here"
     git push origin your-feature-branch
     ```
7. **Install the Package from Your Git Repository**
   - You can now install the package from your forked repository using pip. You can use the URL of your forked repository:
     ```bash
     pip install git+https://github.com/your-username/repo-name.git@your-feature-branch
     ```
   - Replace your-username with your GitHub username, repo-name with the repository name, and your-feature-branch with the name of the branch where you made your changes.

  ## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.

### Summary

- **Permissions:** Allows use, distribution, and creation of derivative works, subject to the conditions.
- **Conditions:** Must include a copy of the license in redistributions, provide a notice of changes, and include a copy of the NOTICE file.
- **Limitation:** The software is provided "as is", without warranties or conditions of any kind.

For more details, please refer to the full [Apache License 2.0 text](https://www.apache.org/licenses/LICENSE-2.0).

