import requests
import json
from app.config import BASE_URL, API_KEY, API_SECRET

headers = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

def get_sales_order_status(order_id):
    """Fetches status for IDs like SAL-ORD-2026-00001"""
    url = f"{BASE_URL}/api/resource/Sales Order/{order_id}"
    try:
        res = requests.get(url, headers=headers, timeout=5)
        return res.json().get("data", {}).get("status", "Not Found") if res.status_code == 200 else "Not Found"
    except:
        return "Connection Error"

def get_purchase_order_status(order_id):
    """Fetches status for IDs like PUR-ORD-2026-00006"""
    url = f"{BASE_URL}/api/resource/Purchase Order/{order_id}"
    try:
        res = requests.get(url, headers=headers, timeout=5)
        return res.json().get("data", {}).get("status", "Not Found") if res.status_code == 200 else "Not Found"
    except:
        return "Connection Error"

def get_employee_status(name):
    """Searches for an employee by name and returns their status"""
    params = {"filters": json.dumps([["employee_name", "like", f"%{name}%"]])}
    url = f"{BASE_URL}/api/resource/Employee"
    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        data = res.json().get("data", [])
        return "Active" if data else "Not Found"
    except:
        return "Connection Error"
