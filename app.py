import os
import logging
import resend
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

resend.api_key = os.getenv('RESEND_API_KEY')
NOTIFY_EMAIL = os.getenv('EMAIL_ADDRESS')

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')

app = Flask(__name__)
CORS(app, origins=["https://rico-portfolio-wine.vercel.app"])

@app.route('/contact', methods=['POST'])
def contact():
    first_name = request.form.get('first name')
    last_name = request.form.get('last name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not first_name or not last_name or not email or not message:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        send_email(first_name, last_name, email, message)
    except Exception as e:
        print(f"Failed to send Email: {e}")
        return jsonify({"error": "Failed to send Email"}), 500

    print(f"New message from {first_name} {last_name} ({email}): {message}")
    return jsonify({'status': 'success', 'message': 'Form received'}), 200

def send_email(first_name, last_name, email, message):
    body = f"Name: {first_name} {last_name}\nEmail: {email}\n\nMessage:\n{message}"

    resend.Emails.send({
        "from": "Portfolio Contact <onboarding@resend.dev>",
        "to": [NOTIFY_EMAIL],
        "subject": f"New portfolio message from {first_name} {last_name}",
        "text": body,
        "reply_to": email,
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
