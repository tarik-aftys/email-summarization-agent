import os
import json
import base64
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
TOKEN_FILE = os.path.join(CONFIG_DIR, "token.json")
CLIENT_SECRET_FILE = os.path.join(CONFIG_DIR, "client_secret.json")
MAX_RESULTS = 10

os.makedirs(CONFIG_DIR, exist_ok=True)

def get_credentials():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return creds

def get_message_content(access_token, message_id):

    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"format": "full"}

    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def decode_email_body(message_data):

    body_text = ""
    
    payload = message_data.get("payload", {})
    
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data", "")
                if data:
                    body_text = base64.urlsafe_b64decode(data).decode("utf-8")
                    break
            elif part.get("mimeType") == "text/html":
                data = part["body"].get("data", "")
                if data and not body_text:
                    body_text = base64.urlsafe_b64decode(data).decode("utf-8")
    else:
        if payload.get("mimeType") == "text/plain":
            data = payload["body"].get("data", "")
            if data:
                body_text = base64.urlsafe_b64decode(data).decode("utf-8")
    
    return body_text

def extract_email_info(message_data):

    headers = message_data.get("payload", {}).get("headers", [])
    
    email_info = {
        "id": message_data.get("id"),
        "threadId": message_data.get("threadId"),
        "snippet": message_data.get("snippet", ""),
        "subject": "",
        "from": "",
        "date": "",
        "body": decode_email_body(message_data)
    }
    
    for header in headers:
        name = header.get("name", "").lower()
        value = header.get("value", "")
        
        if name == "subject":
            email_info["subject"] = value
        elif name == "from":
            email_info["from"] = value
        elif name == "date":
            email_info["date"] = value
    
    return email_info

def list_last_messages(access_token):

    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"maxResults": MAX_RESULTS}
    emails_with_content = []

    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    messages_list = r.json()
    
    for msg in messages_list.get("messages", []):
        message_id = msg["id"]
        message_data = get_message_content(access_token, message_id)
        email_info = extract_email_info(message_data)
        emails_with_content.append(email_info)
    
    return emails_with_content

def save_emails_to_file(emails, filepath="outputs/emails.txt"):
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        for i, email in enumerate(emails, 1):

            f.write(f"EMAIL {i}\n")
            f.write(f"ID: {email.get('id', 'N/A')}\n")
            f.write(f"Sender: {email.get('from', 'N/A')}\n")
            f.write(f"Subject: {email.get('subject', 'N/A')}\n")
            f.write(f"Date: {email.get('date', 'N/A')}\n")
            f.write(f"Thread ID: {email.get('threadId', 'N/A')}\n")
            f.write(f"Snippet: {email.get('snippet', 'N/A')}\n\n")
            f.write("Body:\n")
            f.write(email.get('body', 'No content available') + "\n\n")
