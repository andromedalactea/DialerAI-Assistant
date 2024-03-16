# Python libraries
import os

# Third-party libraries
from flask import Flask, request, jsonify
from pyngrok import ngrok
from dotenv import load_dotenv

# Local libraries
from class_iris_interaction import IrisCRM

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
ngrok.set_auth_token(os.getenv('NGROK_KEY'))

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint that receives POST requests.
    """
    data = request.json
    # Check if it's the end of the call 'end-of-call-report'
    message_vapi = data.get('message')

    if message_vapi.get('type') == 'end-of-call-report':

        # Extract the necessary information to save a history
        id_lead = message_vapi.get('call').get('customerId')
        phone_number = message_vapi.get('call').get('customer').get('number')
        date = message_vapi.get('call').get('updatedAt').split('.')[0]
        ended_reason = message_vapi.get('endedReason')
        transcript = message_vapi.get('transcript')
        summary = message_vapi.get('summary')

        # Save the information as a note in the specific lead
        iris = IrisCRM()
        response = iris.create_note_for_lead(id_lead, phone_number, date, ended_reason, transcript, summary)

        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "ignored"}), 200


if __name__ == '__main__':
    # Define the port of your choice, by default Flask uses port 5000
    port = 5000

    # Configure ngrok with the port on which Flask is running
    ngrok_tunnel = ngrok.connect(port)
    print('NGROK Tunnel URL:', ngrok_tunnel.public_url)

    # Run the Flask server, making sure it is publicly accessible and on the correct port
    app.run(ssl_context='adhoc', host='0.0.0.0', port=5000)

    # Disconnect the ngrok tunnel when you are ready to end the session
    ngrok.disconnect(ngrok_tunnel.public_url)
