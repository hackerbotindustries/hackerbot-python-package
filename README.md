
# Hackerbot Python Package

Hackerbot python package (`hackerbot-python-package`) is a project that includes modules for controlling and managing the Hackerbot system.

## Installation

Follow these steps to clone the repository and set up the required dependencies.

### 1. Clone the Repository
Use SSH to clone the repository:
```bash
https://github.com/hackerbotindustries/hackerbot-python-package.git
```
This will create a directory named `hackerbot-python-package` and download all necessary files.

### 2. Navigate to the Modules Directory
Move into the `hackerbot_modules` directory:
```bash
cd hackerbot-python-package/
```

### 3. Install Dependencies
Install the `hackerbot` package using `pip`:
```bash
pip install .
```
This will install the package locally for your Python environment.

## Usage
Once installed, you can import `hackerbot` in your Python scripts:
```python
import hackerbot
```

### 4. Testing
To run the unit tests run:
```bash
cd tests/unit_tests
pytest
```

## Troubleshooting
If you run into issues with the installation, try the following:
- Ensure you're using a virtual environment:  
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- Upgrade `pip` before installation:  
  ```bash
  pip install --upgrade pip
  ```
