import subprocess
import sys

def show_signin(current_app=None):
    subprocess.Popen([sys.executable, "StockSmart/LoginPage.py"])
    if current_app:
        current_app.after(100, current_app.destroy)

def show_signup(current_app=None, role="Employee"):
    subprocess.Popen([sys.executable, "StockSmart/SignUpPage.py", role])
    if current_app:
        current_app.after(100, current_app.destroy)

def show_startpage(current_app=None):
    subprocess.Popen([sys.executable, "StockSmart/StartPage.py"])
    if current_app:
        current_app.after(100, current_app.destroy)

def show_dashboard(current_app=None, role="Admin", email="", user_id=None):
    if current_app:
        current_app.destroy()
    subprocess.Popen([sys.executable, "StockSmart/Dashboard.py", email, role,  str(user_id) if user_id is not None else ""])

def show_inventory(current_app=None):
    subprocess.Popen([sys.executable, "StockSmart/inventoryy.py"])
    if current_app:
        current_app.after(100, current_app.destroy)

def show_items(current_app=None):
    subprocess.Popen([sys.executable, "StockSmart/items.py"])
    if current_app:
        current_app.after(100, current_app.destroy)

def show_history_logs(current_app=None):
    subprocess.Popen([sys.executable, "StockSmart/history_log.py"])
    if current_app:
        current_app.after(100, current_app.destroy) 