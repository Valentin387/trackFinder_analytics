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

The program supports saving fetched data to local `.pickle` files for faster access. This feature eliminates the need to repeatedly query the database for the same date range, significantly improving performance.

### How It Works

1. **Exported File Naming**  
   Data fetched for a specific date range is saved in the `local_exports` folder. The file is named using the format:

   ```
   local_exports/<start_date>_to_<end_date>.pickle
   ```

2. **Automatic Validation**  
   Before querying the database, the program checks if a corresponding `.pickle` file already exists in `local_exports`:
   - If the file exists, the program prompts you to either use the local file or overwrite it with new data.
   - If no file exists, the program fetches data from the database and saves it as a new `.pickle` file.

3. **Performance Boost**  
   Utilizing saved `.pickle` files skips the database query step, making data retrieval significantly faster.

### Folder Structure

Ensure your project includes the `local_exports` directory. If it doesn't exist, the program will create it automatically.

```
project_root/
├── local_exports/
├── main.py
├── data/
└── other_files...
```

### Example Workflow

1. **First Run (No Export File Exists)**
   - The program fetches data for the selected date range from MongoDB.
   - The data is saved as a `.pickle` file in `local_exports`.

2. **Subsequent Runs (Export File Exists)**
   - The program detects the `.pickle` file for the selected date range.
   - You will be prompted to either:
     - Use the existing file for faster access, or
     - Overwrite the file by re-fetching data from the database.

---

## Usage

Run the script using:

```bash
python main.py
```

Ensure your `.env` file is correctly set up and that you have activated your virtual environment before running the script.

---

## License

This project is licensed under the MIT License.
