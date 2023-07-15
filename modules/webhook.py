import requests
import json

#send data to webhook as form data, which allows attachments
def send_to_webhook(webhook_url, content, username=None, attachments={}):
  #handle regular json payload
  payload = {
    "content": content,
  }
  if username:
    payload["username"] = username
  
  if not attachments:
    r = requests.post(webhook_url, json=payload)
    return

  #handle form data for attachments
  files = {
    "payload_json": (None, json.dumps(payload), "application/json")
  }
  count = 0
  for filename, contents in attachments.items():
    files[f"files[{count}]"] = (filename, contents)
  
  r = requests.post(webhook_url, files=files)