import os
import requests
from dotenv import load_dotenv


# Chage the environment variables
load_dotenv()

def call_ai(id_lead, phone_number, phoneNumberId="c976502a-22c5-4f10-9aa0-36bd075d473b", assistant_id="6ea5c51c-7adb-441e-9265-485aee43cae2"):
    """
    Calls the AI assistant using the VAPI API.

    Args:
      customer_id (str): The ID of the customer.
      phone_number (str): The phone number to call.
      assistant_id (str, optional): The ID of the assistant. Defaults to "6ea5c51c-7adb-441e-9265-485aee43cae2".

    Returns:
      None
    """
    token_vapi = os.getenv('VAPI_KEY')
    url = "https://api.vapi.ai/call/phone"
    payload = {
      "phoneNumberId": phoneNumberId,
      "customer": {
        "number": phone_number
      },
      "assistantId": assistant_id,
      "metadata": {
          "id_lead": id_lead
      }
    }
    headers = {
      "Authorization": f"Bearer {token_vapi}",
      "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return "Call made" if response.status_code == 200 else "Error making the call"

# Example usage:
if __name__ == "__main__":
    id_lead = "11412"
    phone_number = "+16179702027"
    print(call_ai(id_lead, phone_number))

