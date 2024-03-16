# AI-Powered Dialer System

This repository contains the implementation of two microservices designed to enhance lead management through automated AI-powered calls. It connects with the IRIS CRM to fetch necessary information and then interacts with leads using the VAPI API for managed calls.

## Microservices Overview

### 1. IRIS CRM Interaction Service
Located at `scripts/main.py`, this service fetches leads from the IRIS CRM based on specified categories and statuses. It extracts names and phone numbers, then initiates AI-managed calls to each lead via the VAPI API.

#### Main Features:
- Fetching lead information from IRIS CRM.
- Initiating outbound calls to leads with AI assistance.

### 2. VAPI Webhook Receiver
Implemented in `scripts/webhook_vapi.py`, this Flask application acts as a webhook to receive data on calls made by the first microservice. If a call is reported as completed, it invokes the IRIS API to add a note to the lead with relevant call information.

#### Main Features:
- Receiving call data through webhook.
- Updating lead information in IRIS CRM based on call outcomes.

## Setup and Configuration

### Requirements
- Python 3.8+
- Flask
- ngrok 
- IRIS CRM and VAPI API access

### Installation
1. Clone this repository to your local machine.
2. Install dependencies from the `requirements.txt` file using pip:
    ```
    pip install -r requirements.txt
    ```
3. Configure the environment variables by creating a `.env` file in the root directory and setting the following keys:
    ```
    X_API_KEY_IRIS_CRM=<your_iris_crm_api_key>
    VAPI_KEY=<your_vapi_api_key>
    NGROK_KEY=<your_ngrok_auth_token>
    ```

### Running the Services

#### IRIS CRM Interaction Service
Execute the `main.py` script to start processing leads:
```bash
python3 scripts/main.py
```



#### VAPI Webhook Receiver
Run the `webhook_vapi.py` script to start the Flask server and receive webhook events:

```bash
python3 scripts/webhook_vapi.py
```



## ngrok Tunneling
To expose your local webhook to the internet, `ngrok` is used. Ensure that your `NGROK_KEY` is correctly set in the `.env` file. Upon running the webhook receiver, an ngrok tunnel URL will be printed to the console, which should be configured in your VAPI dashboard.

## Contribution
Contributions are welcome. Please feel free to submit pull requests or open issues to suggest improvements or add new features.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
