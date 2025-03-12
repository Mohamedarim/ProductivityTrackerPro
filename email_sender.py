import smtplib
from email.message import EmailMessage
import os

def send_email(to_email, report_file):
    from_email = 'mohamedamin30071@gmail.com'
    app_password = 'idrk qanh lykt obdy'

    msg = EmailMessage()
    msg['Subject'] = 'Daily Productivity Report'
    msg['From'] = from_email
    msg['To'] = to_email

    msg.set_content('Attached is your daily productivity report.')

    with open(report_file, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(report_file)

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)
        print(f"✅ Report sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
