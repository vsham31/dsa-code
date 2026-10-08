# Simple RAG Project

This repository contains a simple Retrieval-Augmented Generation (RAG) system built with Python, using `sentence-transformers` for embeddings, `scikit-learn` for similarity matching, and the official `google-genai` SDK for generation.

## Getting Started

Follow these step-by-step instructions to set up your environment and run the application on Ubuntu.

### 1. Install Pre-requisites
Ubuntu requires the specific virtual environment package for your Python version. Install it by running:
```bash
sudo apt install python3.12-venv
```

### 2. Create a Virtual Environment
Create an isolated environment named `.venv` to manage your dependencies safely:
```bash
python3 -m venv .venv
```

### 3. Activate the Environment
Activate the virtual environment before installing packages or running the script:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
Install all required libraries listed in the `requirements.txt` file:
```bash
pip3 install -r requirements.txt
```

### 5. Run the Application
Execute the primary script to start the RAG workflow:
```bash
python3 simple_rag.py
```
