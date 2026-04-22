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
    url = os.getenv("LLM_API_URL")
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not url or not api_key:
        raise HTTPException(status_code=500, detail="Missing API configuration")

    system_prompt = """
    You are an ERP Data Extractor.
    Extract Category (SALES, PURCHASE, EMPLOYEE) and subject.
    Return ONLY JSON like:
    {"category": "SALES", "subject": "SAL-ORD-2026-00001"}
    """

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        "response_format": {"type": "json_object"}
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        response.raise_for_status()

        res_data = response.json()

        if "choices" not in res_data:
            print("INVALID AI RESPONSE:", res_data)
            return "AI response error"

        ai_content = res_data['choices'][0]['message']['content'].strip()
        print("AI RAW:", ai_content)

        try:
            result = json.loads(ai_content)
        except json.JSONDecodeError:
            return "Could not understand the query."

        category = result.get("category", "").upper()
        subject = result.get("subject", "")

        if not category or not subject:
            return "Please provide a valid query."

        handlers = {
            "PURCHASE": (get_purchase_order_status, "Purchase Order {subject} is {status}"),
            "SALES": (get_sales_order_status, "Sales Order {subject} is {status}"),
            "EMPLOYEE": (get_employee_status, "Employee {subject} is {status}")
        }

        if category not in handlers:
            return "Unknown request type."

        fetch_func, template = handlers[category]

        try:
            status = fetch_func(subject)
        except Exception as e:
            print("ERP ERROR:", str(e))
            return f"Could not fetch data for {subject}"

        return template.format(subject=subject, status=status)

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="AI service timeout")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API error: {str(e)}")

    except Exception as e:
        print("FINAL ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")
