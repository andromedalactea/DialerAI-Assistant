import os
import requests

token_vapi = os.getenv('TOKEN_VAPI')
url = "https://api.vapi.ai/call/phone"

payload = {
  "phoneNumberId": "c976502a-22c5-4f10-9aa0-36bd075d473b",
  "customer": {
    "number": "+18572689278"
  },
    "assistantId": "6ea5c51c-7adb-441e-9265-485aee43cae2",
    "customer": {
        "extension": "<string>",
        "name": "<string>",
        "number": "<string>"
    },
    "serverUrl": "https://eo18q392z2n06jq1m.pipedream.com",

    "serverMessages": [
      "end-of-call-report",
      "status-update",
      "hang",
      "function-call"
    ]
}
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)