import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import smtplib
from email.mime.text import MIMEText

# Email sending logic
def send_email(subject, body, recipient_email):
    sender_email = os.environ.get("EMAIL_USER")  # Grab Gmail address
    sender_password = os.environ.get("EMAIL_PASS")  # Grab App Password

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("✅ Email sent successfully")
        return True
    except Exception as e:
        print("❌ Failed to send email:", e)
        return False


# HTTP server to receive form data
class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/contact":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            form_data = parse_qs(post_data)

            name = form_data.get("name", [""])[0]
            email = form_data.get("email", [""])[0]
            message = form_data.get("message", [""])[0]

            # Format email body
            subject = f"New Contact Form Submission from {name}"
            body = f"From: {name} <{email}>\n\nMessage:\n{message}"

            # You can change this to your church email or keep it dynamic
            recipient = os.environ.get("CONTACT_RECEIVER", "redeemedgospelchurchsubukia@gmail.com")

            success = send_email(subject, body, recipient)

            self.send_response(200 if success else 500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Message sent!" if success else b"Failed to send email.")
        else:
            self.send_error(404, "Not Found")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
            <form method="POST" action="/contact">
                <input name="name" placeholder="Your Name"><br>
                <input name="email" placeholder="Your Email"><br>
                <textarea name="message" placeholder="Your Message"></textarea><br>
                <button type="submit">Send</button>
            </form>
        """)


# Server setup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render sets PORT automatically
    server = HTTPServer(("", port), SimpleHandler)
    print(f"🚀 Server running on port {port}...")
    server.serve_forever()
