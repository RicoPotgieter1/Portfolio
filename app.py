import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

app = Flask(__name__)
CORS(app)

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
    subject = f"New portfolio message from {first_name} {last_name}"
    body = f"Name: {first_name} {last_name}\nEmail: {email}\n\nMessage:\n{message}"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['TO'] = EMAIL_ADDRESS
    msg['Reply-To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(port=5000, debug=True)