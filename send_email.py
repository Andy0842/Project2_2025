# Test Sending Emails with Python
# Date 22/4/2025
# Student ID 202283890018 W20109667
# Author Yang Yue

import smtplib
from email.message import EmailMessage

# Sender email configuration
from_email_addr = "nuist_202283890018@163.com"
from_email_pass = "GNM9umMuUfxHTKaG"
to_email_addr = "nuist_202283890018@163.com"

# Create email message object
msg = EmailMessage()

# Set email body content
body = "Hello from Raspberry Pi"
msg.set_content(body)

# Set sender and recipient
msg['From'] = from_email_addr
msg['To'] = to_email_addr

# Set email subject
msg['Subject'] = 'TEST EMAIL'

try:
    # Connect to SMTP server (using Gmail as example)
    server = smtplib.SMTP()
    server.connect("smtp.163.com",25)
    # Enable TLS encryption
    #server.starttls()
    
    # Login to email account
    server.login(from_email_addr, from_email_pass)
    
    # Send the email
    server.send_message(msg)
    print('Send successfully')
    server.quit()

except Exception as e:
    print(f'Send failed: {str(e)}')
    server.quit()
