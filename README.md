# trackFinder_analytics
Simple python project to fetch and study data from a mongo db database. Generate informs to get insights

# Project Setup

## Setting Up the Project

### Step 1: Create a `.env` File

It is recommended to use a virtual environment to manage the project's dependencies. To create and activate a virtual environment, follow these steps:

1. **Create the virtual environment:**

   On Windows:
   ```bash
   python -m venv venv

Then create a `.env` file in the root of the project. Then, add the following content:

```env
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

Make sure to replace the placeholders with your actual MongoDB credentials. Also, ensure the .env file is not committed by adding it to your .gitignore:

### Step 2: Install Dependencies
To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Local Data Export and Retrieval

### Overview
The program now supports saving fetched data to local `.pickle` files for faster subsequent access. This feature reduces the need to re-fetch data from the database for the same date range, improving performance.

### How It Works
1. **Exported File Naming**:  
   After fetching documents from the database for a specific date range, the program stores the data in the `local_exports` folder. The file is named based on the selected date range using the format:  

   ```bash
   local_exports/<start_date>_to_<end_date>.pickle
   ```

2. **Automatic Validation**:  
   Before querying the database, the program checks if a corresponding `.pickle` file already exists in the `local_exports` folder for the selected date range:
   - If the file exists, the program asks whether to use the local data or overwrite it with new data from the database.
   - If the file does not exist, the program fetches data from the database and saves it to a new `.pickle` file.

3. **Improved Performance**:  
   By utilizing saved `.pickle` files, the program skips the time-consuming process of querying the database and converting documents to Python objects.

### Folder Structure
Ensure your project folder contains the `local_exports` directory. If it doesn’t exist, the program will create it automatically.

```
project_root/
├── local_exports/
├── main.py
├── data/
└── other_files...
```

### Example Workflow
1. **First Run (No Export File Exists)**:
   - The program fetches data for the selected date range from the database.
   - The data is saved in a `.pickle` file within the `local_exports` folder.

2. **Subsequent Runs (Export File Exists)**:
   - The program detects the `.pickle` file for the selected date range.
   - You will be prompted to choose whether to:
     - Use the saved file for faster access, or
     - Overwrite the file by re-fetching data from the database.
