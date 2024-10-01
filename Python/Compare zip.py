import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from deepdiff import DeepDiff

def lambda_handler(event, context):
    # Define file paths
    file1_path = '/var/task/js1.json'
    file2_path = '/var/task/js2.json'
    
    # Load JSON data
    try:
        with open(file1_path, 'r') as file1:
            data1 = json.load(file1)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error loading {file1_path}: {str(e)}')
        }
    
    try:
        with open(file2_path, 'r') as file2:
            data2 = json.load(file2)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error loading {file2_path}: {str(e)}')
        }
    
    # Compare JSON files
    diff = DeepDiff(data1, data2, verbose_level=2)
    
    if diff:
        subject = 'JSON Files Difference Detected'
        body = f'Differences between {file1_path} and {file2_path}:\n\n{json.dumps(diff, indent=2)}'
        email_sent = send_email(subject, body)
        
        if email_sent:
            return {
                'statusCode': 200,
                'body': json.dumps('Differences found and email sent.')
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps('Differences found, but failed to send email.')
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('No differences found.')
        }

def send_email(subject, body):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_password = 'wjaepndnxmujglvweuh;dsihc'
        smtp_username = 'mail'
        sender_email = 'mail'
        recipient_email = 'mail_ids'

        # Create message container
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach body with the msg instance
        message.attach(MIMEText(body, 'plain'))

        # Send the message via SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        
        return True
    except Exception as e:
        print(f'Failed to send email: {str(e)}')
        return False
