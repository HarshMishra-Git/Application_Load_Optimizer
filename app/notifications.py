import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email(subject, body, to_email):
    from_email = "harsh.mishra2022@glbajajgroup.org"  # Replace with your email address
    from_password = "qstw etsv mzvr xaso"  # Replace with your app-specific password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_notification(method, message, recipient_email, details=""):
    if method == "Email":
        subject = "Notification from Application Load Analyzer"
        body = f"Hello,\n\n{message}\n\nDetails:\n{details}\n\nBest regards,\nApplication Load Analyzer"
        send_email(subject, body, recipient_email)