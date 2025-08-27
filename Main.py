import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("VAPI_API_KEY")
BASE_URL = "https://api.vapi.ai"  # Correct base URL

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 1. Update Assistant Instructions (Optional, only if you need to modify the existing assistant)
def update_assistant(assistant_id):
    payload = {
        "name": "Pizza Order Agent",
        "voice": "alloy",
        "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": 0.7
        },
        "firstMessage": "Welcome to our Pizza Restaurant! How can I assist you with your order today?",
        "assistantOverrides": {
            "instructions": """
You are a friendly Pizza Restaurant Order Taking Assistant.
Steps:
1. Greet politely (handled by firstMessage).
2. Take order (pizza type, size, toppings).
3. Confirm and repeat back the order with the total price.
4. Thank the customer and provide an estimated delivery time (e.g., 30 minutes).
Menu:
- Margherita: Small $10, Medium $15, Large $20
- Pepperoni: Small $12, Medium $17, Large $22
- Veggie Delight: Small $11, Medium $16, Large $21
- Toppings: Cheese $2, Olives $1, Mushrooms $1.5
"""
        }
    }
    try:
        response = requests.patch(f"{BASE_URL}/assistant/{assistant_id}", headers=headers, json=payload)
        response.raise_for_status()
        print(f"✅ Assistant Updated: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to update assistant: {e}")
        return None

# 2. Get Phone Number Details (for verification)
def get_phone_number(phone_number_id):
    try:
        response = requests.get(f"{BASE_URL}/phone-number/{phone_number_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get phone number details: {e}")
        return None

if __name__ == "__main__":
    # Use existing assistant and phone number IDs
    assistant_id = "99abf62e-8a93-4962-ba07-21553bd31392"  # From your GET response
    phone_number_id = "b58f77b3-f30a-4c46-9a67-189be147e8d1"  # From your GET response

    # Step 1: Verify phone number assignment
    phone_details = get_phone_number(phone_number_id)
    if phone_details and phone_details.get('assistantId') == assistant_id:
        print(f"✅ Phone number {phone_details.get('number')} is active and assigned to Pizza Order Agent")
    else:
        print(f"❌ Phone number assignment verification failed: {phone_details}")

    # Step 2: Optionally update assistant instructions (uncomment if needed)
    # updated_assistant = update_assistant(assistant_id)
    # if updated_assistant:
    #     print(f"✅ Assistant Configuration Updated: {updated_assistant}")
    # else:
    #     print("❌ Failed to update assistant")