# 📦 Streamlit App Starter Kit 

# Project Setup

## Prerequisites

Ensure you have Python installed on your system. You can download the latest version from [python.org](https://www.python.org/downloads/).

## Setting Up the Environment

It is recommended to use a virtual environment to manage dependencies. Follow these steps to set up and install the required packages:

### 1. Create a Virtual Environment

**On macOS/Linux:**
```sh
python3 -m venv venv
```

**On Windows:**
```sh
python -m venv venv
```

### 2. Activate the Virtual Environment

**On macOS/Linux:**
```sh
source venv/bin/activate
```

**On Windows (Command Prompt):**
```sh
venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies:
```sh
pip install -r requirements.txt
```

## Running the Project

After installing the dependencies, you can run the project using:
```sh
streamlit run streamlit_app.py 
```

## Deactivating the Virtual Environment

To exit the virtual environment, simply run:
```sh
deactivate
```

## Additional Notes

- If `pip` is outdated, upgrade it using:
  ```sh
  pip install --upgrade pip
  ```
- If you encounter issues with dependencies, try recreating the virtual environment by deleting the `venv` folder and following the setup steps again.

---



