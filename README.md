Phase 1: OS & Environment Setup
These commands prepare the Windows Subsystem for Linux (WSL) and install the necessary Python tools.

# 1. Install WSL and Ubuntu (Run in Windows PowerShell as Admin)
wsl --install

# 2. Update Linux packages (Run in Ubuntu Terminal)
sudo apt update && sudo apt upgrade -y

# 3. Install Python 3 and Virtual Environment tools
sudo apt install python3-pip python3-venv -y

Phase 2: Project Architecture Creation
This set of commands builds the professional directory tree for "Code Casters."

# 1. Create the project root and navigate into it
mkdir -p ~/erp-ai-chatbot && cd ~/erp-ai-chatbot

# 2. Create the Backend and Frontend folders
mkdir -p backend/app frontend

# 3. Create the Backend files
touch backend/.env backend/requirements.txt
touch backend/app/__init__.py backend/app/main.py backend/app/chatbot.py backend/app/erp_api.py backend/app/config.py

# 4. Create the Frontend files
touch frontend/index.html frontend/style.css frontend/script.js

Phase 3: The Detailed Folder Structure
After running the commands above, your project will look exactly like this. Use this tree for your README and Project Report.

erp-ai-chatbot/
├── backend/                # Server-side logic (FastAPI)
│   ├── .env                # Secret API Keys (OpenRouter)
│   ├── requirements.txt    # Python library list
│   ├── venv/               # Virtual Environment (Isolated libraries)
│   └── app/
│       ├── __init__.py     # Makes 'app' a Python package
│       ├── main.py         # API Endpoints & CORS settings
│       ├── chatbot.py      # AI Processing (Gemini logic)
│       ├── erp_api.py      # ERPNext connection functions
│       └── config.py       # Configuration settings
└── frontend/               # Client-side interface
    ├── index.html          # Web page structure
    ├── style.css           # UI Design & Styling
    └── script.js           # API communication logic

Phase 4: Backend Implementation Commands
Prepare the Python environment to handle the AI and ERP requests.

# 1. Enter backend and setup Virtual Environment
cd ~/erp-ai-chatbot/backend
python3 -m venv venv
source venv/bin/activate

# 2. Install required libraries
pip install fastapi uvicorn requests python-dotenv

# 3. Save the dependencies to your requirements file
pip freeze > requirements.txt

Phase 5: Launch & Execution
To run the full-stack application, you must keep two terminal windows open simultaneously.

Terminal A: The Backend (FastAPI)

cd ~/erp-ai-chatbot/backend
source venv/bin/activate
uvicorn app.main:app --reload

Terminal B: The Frontend (Python Web Server)

cd ~/erp-ai-chatbot/frontend
python3 -m http.server 5500
