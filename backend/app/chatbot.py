import re
import os
import json
import requests
from fastapi import HTTPException
from app.erp_api import (
    get_sales_order_status,
    get_employee_status,
    get_purchase_order_status
)

def get_response(query: str):
    url = os.getenv("url")
    api_key = os.getenv("OPENROUTER_API_KEY")

    # The AI prompt for the queries including the example pucharse and sales ID.
    system_prompt = """
    You are an ERP Data Extractor.
    Your task is to extract the Category (SALES, PURCHASE, or EMPLOYEE) and the EXACT ID or Name.
    Examples:
    - Query: 'Status of PUR-ORD-2026-00006' -> {"category": "PURCHASE", "subject": "PUR-ORD-2026-00006"}
    - Query: 'What about SAL-ORD-2026-00001' -> {"category": "SALES", "subject": "SAL-ORD-2026-00001"}
    - Query: 'Is Arjun active?' -> {"category": "EMPLOYEE", "subject": "Arjun"}

    Return ONLY JSON. No conversation.
    """

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        "response_format": { "type": "json_object" }
    }

    headers = { "Authorization": f"Bearer {api_key}", "Content-Type": "application/json" }

    try:
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()
        ai_content = res_data['choices'][0]['message']['content'].strip()
        result = json.loads(ai_content)
        category = result.get("category", "").upper()
        subject = result.get("subject", "")
	handlers = {
            "PURCHASE": (get_purchase_order_status, "Purchase Order Found: {subject} is {status}"),
            "SALES": (get_sales_order_status, "Sales Order Found: {subject} is {status}"),
            "EMPLOYEE": (get_employee_status, "Employee Check: {subject} is currently {status}")
        }
        if category in handlers:
            fetch_func, template = handlers[category]
            status = fetch_func(subject)
            return template.format(subject=subject, status=status)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")

    return "I couldn't identify the specific ID. Please provide the full ID (e.g., PUR-ORD-2026-00006)."
