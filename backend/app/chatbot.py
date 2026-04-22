import re
import os
import json
import requests
from app.erp_api import (
    get_sales_order_status,
    get_employee_status,
    get_purchase_order_status
)

def get_response(query: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    api_key = os.getenv("OPENROUTER_API_KEY")

    # The "Few-Shot" prompt gives the AI clear examples of your ID formats
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
        # Extract and parse the content
        ai_content = res_data['choices'][0]['message']['content'].strip()
        print(f"DEBUG AI RESULT: {ai_content}") # Watch this in your terminal

        result = json.loads(ai_content)
        category = result.get("category", "").upper()
        subject = result.get("subject", "")

        # Routing to your ERP functions
        if category == "PURCHASE":
            status = get_purchase_order_status(subject)
            return f"Purchase Order Found: {subject} is {status}"
        elif category == "SALES":
            status = get_sales_order_status(subject)
            return f"Sales Order Found: {subject} is {status}"
        elif category == "EMPLOYEE":
            status = get_employee_status(subject)
            return f"Employee Check: {subject} is currently {status}"

    except Exception as e:
        return f"System Error: {str(e)}"

    return "I couldn't identify the specific ID. Please provide the full ID (e.g., PUR-ORD-2026-00006)."
