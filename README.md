# ERPNext AI Chatbot Assistant

This project sets up an AI chatbot integrated with an ERPNext backend. The backend connects to the ERPNext REST API to query data, and a frontend interface provides a user-friendly UI for interactions.

## Phase 1: OS & Environment Setup

These commands prepare the Windows Subsystem for Linux (WSL) and install the necessary Python tools.

1. **Install WSL and Ubuntu** (Run in Windows PowerShell as Admin):
   ```powershell
   wsl --install
   ```

2. **Update Linux packages** (Run in Ubuntu Terminal):
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Install Python 3 and Virtual Environment tools**:
   ```bash
   sudo apt install python3-pip python3-venv -y
   ```

## Phase 2: ERPNext Infrastructure Setup (MariaDB, Frappe, ERPNext)

Before building the chatbot, you need a local instance of ERPNext running. The following commands install the required database (MariaDB), the framework (Frappe), and the application (ERPNext).

1. **Install MariaDB, Redis, and required dependencies**:
   ```bash
   sudo apt install mariadb-server mariadb-client redis-server curl software-properties-common nano -y
   ```

2. **Configure MariaDB**:
   Secure the database installation (set a root password when prompted):
   ```bash
   sudo mysql_secure_installation
   ```
   Add Frappe's required database settings by editing the MariaDB config:
   ```bash
   sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
   ```
   *Optional If any error occurs - (Add the following block to the bottom of the file and save)*
   ```ini
   [mysqld]
   character-set-client-handshake = FALSE
   character-set-server = utf8mb4
   collation-server = utf8mb4_unicode_ci
   ```
   Restart the database service:
   ```bash
   sudo systemctl restart mariadb
   ```

3. **Install Node.js, Yarn, and Python development tools**:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt install -y python3-dev
   sudo npm install -g yarn
   ```

4. **Install Frappe Bench**:
   ```bash
   sudo pip3 install frappe-bench
   ```

5. **Initialize Frappe Bench**:
   ```bash
   cd ~
   bench init --frappe-branch version-15 frappe-bench
   cd frappe-bench
   ```

6. **Create a New Site**:
   ```bash
   bench new-site erpnext.local
   ```

7. **Download and Install ERPNext**:
   ```bash
   bench get-app --branch version-15 erpnext
   bench --site erpnext.local install-app erpnext
   ```

8. **Start your ERPNext server**:
   ```bash
   bench start
   ```

## Phase 3: Project Architecture Creation

This set of commands builds the professional directory tree for your chatbot project.

1. **Create the project root and navigate into it**:
   ```bash
   mkdir -p ~/erp-ai-chatbot && cd ~/erp-ai-chatbot
   ```

2. **Create the Backend and Frontend folders**:
   ```bash
   mkdir -p backend/app frontend
   ```

3. **Create the Backend files**:
   ```bash
   touch backend/.env backend/requirements.txt
   touch backend/app/__init__.py backend/app/main.py backend/app/chatbot.py backend/app/erp_api.py backend/app/config.py
   ```

4. **Create the Frontend files**:
   ```bash
   touch frontend/index.html frontend/style.css frontend/script.js
   ```

## Phase 4: The Detailed Folder Structure

After running the commands above, your project will look exactly like this:

```text
erp-ai-chatbot/
├── backend/                # Server-side logic (FastAPI)
│   ├── .env                # Secret API Keys (OpenRouter/OpenAI, ERPNext Auth)
│   ├── requirements.txt    # Python library list
│   ├── venv/               # Virtual Environment (Isolated libraries)
│   └── app/
│       ├── __init__.py     # Makes 'app' a Python package
│       ├── main.py         # API Endpoints & CORS settings
│       ├── chatbot.py      # AI Processing logic
│       ├── erp_api.py      # ERPNext connection functions
│       └── config.py       # Configuration settings
└── frontend/               # Client-side interface
    ├── index.html          # Web page structure
    ├── style.css           # UI Design & Styling
    └── script.js           # API communication logic
```

## Phase 5: Backend Implementation Commands

Prepare the Python environment to handle the AI and ERP requests.

1. **Enter backend and setup Virtual Environment**:
   ```bash
   cd ~/erp-ai-chatbot/backend
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install required libraries**:
   ```bash
   pip install fastapi uvicorn requests python-dotenv
   ```

3. **Save the dependencies to your requirements file**:
   ```bash
   pip freeze > requirements.txt
   ```

## Phase 6: Launch & Execution

To run the full-stack application, keep two terminal windows open simultaneously.

### Terminal A: The Backend (FastAPI)

```bash
cd ~/erp-ai-chatbot/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Terminal B: The Frontend (Python Web Server)

```bash
cd ~/erp-ai-chatbot/frontend
python3 -m http.server 5500
```
