#Agile Raspberry Pi Plant Moisture Sensor with Email Notification
#This program will send an email every three hours to report the condition of the soil and whether watering is required.
#Date: 23/4/25
#Student ID: 202283890018    W20109667
#Name: Yang Yue


#!/usr/bin/env python3
import RPi.GPIO as GPIO
import smtplib
import time
from email.message import EmailMessage
from datetime import datetime

SENSOR_PIN = 4          
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 25
SENDER_EMAIL = "nuist_202283890018@163.com"
SENDER_PASSWORD = "GNM9umMuUfxHTKaG"  
RECEIVER_EMAIL = "nuist_202283890018@163.com"

TARGET_HOURS = {9, 12, 15, 18, 21}  
last_triggered_hour = -1  

def get_beijing_time():
    """Get time now"""
    return datetime.now().hour, datetime.now().minute

def read_sensor():
    status = GPIO.input(SENSOR_PIN)
    return "dry" if status else "moist", status

def send_email(status_text):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"report {datetime.now().strftime('%H:%M')}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        
        email_body = f"""\
Time：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status：{status_text}
Suggestion：{'Need water' if "dry" in status_text else 'Nothing wrong'}"""

        msg.set_content(email_body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"{time.strftime('%H:%M')} Send successfully")

    except Exception as e:
        print(f"Send failed：{str(e)}")

def check_schedule():
    global last_triggered_hour
    current_hour, current_min = get_beijing_time()
    
    if current_min == 0 and current_hour in TARGET_HOURS:
        if current_hour != last_triggered_hour:
            status_text, _ = read_sensor()
            send_email(status_text)
            last_triggered_hour = current_hour
    else:
        last_triggered_hour = -1  

if __name__ == "__main__":
    try:
        print("System started...")
        while True:
            check_schedule()
            time.sleep(55)  
            
    except KeyboardInterrupt:
        print("\nSystem stopped")
    finally:
        GPIO.cleanup()
