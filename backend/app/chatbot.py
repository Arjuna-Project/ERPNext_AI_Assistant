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
            raise HTTPException(status_code=500, detail="Invalid AI response")

        ai_content = res_data['choices'][0]['message']['content'].strip()

        try:
            result = json.loads(ai_content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON from AI")

        category = result.get("category", "").upper()
        subject = result.get("subject", "")

        if not category or not subject:
            return "Please provide a valid query with ID or name."

        handlers = {
            "PURCHASE": (
                get_purchase_order_status,
                "Purchase Order {subject} is {status}"
            ),
            "SALES": (
                get_sales_order_status,
                "Sales Order {subject} is {status}"
            ),
            "EMPLOYEE": (
                get_employee_status,
                "Employee {subject} is {status}"
            )
        }

        if category in handlers:
            fetch_func, template = handlers[category]

            try:
                status = fetch_func(subject)
                return template.format(subject=subject, status=status)
            except Exception:
                raise HTTPException(status_code=500, detail="Error fetching ERP data")

        return "Unknown request type. Please specify Sales Order, Purchase Order, or Employee."

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="AI service timeout")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")
