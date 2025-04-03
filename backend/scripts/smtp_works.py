# /backend/smtp_works.py

import smtplib
from email.mime.text import MIMEText

# Replace with your actual values
smtp_server = "smtp.zoho.com"
smtp_port = 587
your_email = "admin@fordisludus.com"
your_password = "tHuNZ9bdf4Tr"  # Use app password if 2FA is enabled

to_email = "admin@fordisludus.com"  # Use a test recipient
subject = "SMTP Test from Fordis Ludus"
html_body = "<h1>Hello!</h1><p>This is a test email sent using Zoho SMTP + smtplib.</p>"

# Create MIME message
msg = MIMEText(html_body, "html")
msg["Subject"] = subject
msg["From"] = your_email
msg["To"] = to_email

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(your_email, your_password)
        server.sendmail(your_email, to_email, msg.as_string())
        print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
