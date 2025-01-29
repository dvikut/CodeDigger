# CodeDigger 🕵️‍♂️🔍

**CodeDigger** is a powerful Python tool for indexing and searching **Java codebases efficiently**. It scans Java source files, extracts class names and relevant tokens, and stores them in a searchable dictionary. With **fuzzy search capabilities**, CodeDigger helps developers quickly locate files related to specific keywords, even when exact matches are unavailable.

## ✨ Ideal for Retrieval-Augmented Generation (RAG) on Large Codebases
CodeDigger is particularly useful for **RAG-based applications** where **LLMs (Large Language Models) need efficient code retrieval**. By providing a **fast and structured way** to fetch relevant code snippets, it enhances AI-assisted programming, making it easier to generate, refactor, and understand large codebases.

## 🚀 Features
- **Automatic Indexing**: Parses Java source files and indexes class names, method names, and relevant tokens.
- **Fast Lookup**: Quickly retrieves file locations for any keyword.
- **Fuzzy Matching**: Finds the most similar keywords when exact matches are not found.
- **Persistent Storage**: Saves and loads indexed data using pickle for faster access.
- **Multi-Directory Support**: Can process multiple directories at once.
- **Character Encoding Detection**: Uses chardet to handle different file encodings.
- **🔍 RAG-Friendly**: Works seamlessly with LLM-powered applications by providing structured search results for code retrieval.
## 📌 Usage
1️⃣ Initialize CodeDigger
```python
from codedigger import CodeDigger

directories = ["path/to/codebase"]
code_digger = CodeDigger(directories, codebase_version="v1.0")
```

2️⃣ Index the Java Codebase
```python
code_digger.process_codebase()
```
3️⃣ Lookup a Keyword
```python
files = code_digger.lookup("MyClass")
print(files)  # List of file paths containing 'MyClass'
```
4️⃣ Find Similar Keywords
```python
best_match = code_digger.find_most_similar_keyword("MyClas")  
print(best_match)  # Returns the closest match, e.g., 'MyClass'

similar_keywords = code_digger.find_most_similar_keywords("MyClas", threshold=80)
print(similar_keywords)  # Returns a list of similar keywords
```
## 🛠 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/dvikut/CodeDigger.git
cd CodeDigger
pip install -r requirements.txt
```
## 🏗️ How It Works
- **Reads Java Files**: Scans .java files in the provided directories.
- **Extracts Tokens**: Identifies class names and significant code elements.
- **Stores Index**: Saves the extracted data in a dictionary.
- **Search & Suggest**: Allows exact keyword lookup or fuzzy matching for similar terms.
- **Integrates with RAG Pipelines**: Enables fast, structured retrieval for LLM-powered code generation.
## 🏆 Why Use CodeDigger?
- **Speeds up code search** in large projects.
- **Enhances RAG-powered AI assistants** by providing precise code lookups.
- **Works offline** with stored dictionaries for quick access.
- **Supports massive codebases**, making it a great fit for **enterprise-scale** AI coding tools.
## 📝 License
This project is licensed under the MIT License.

