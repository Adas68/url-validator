REM Step 1: Navigate to your project folder
cd "D:\Summer Project Ideas\2025\url-validator-dependencies"

REM Step 2: Create a virtual environment (if not already created)
python -m venv venv

REM Step 3: Activate the virtual environment
.\venv\Scripts\activate

REM Step 4: Install required dependencies
pip install flask requests

REM Step 5: Make sure data folder and urls.json exist
mkdir data 2>nul
echo {} > data\urls.json

REM Step 6: Run your Flask app
python production_ready_app.py