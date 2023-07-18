#discord webhook wrapper

from modules import extensions, utils

import requests
import json

#send data to webhook as form data, which allows attachments
def send_to_webhook(webhook_url, content, username=None, attachments=[]):
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

  total_size = 0
  index = 0
  for filename, contents in attachments:
    total_size += len(contents)
    if total_size > 25_000_000 or index >= 10:
      break

    files[f"files[{index+1}]"] = (filename, contents)
    index += 1
  
  r = requests.post(webhook_url, files=files)
  #send more than 10 attachments
  if total_size > 25_000_000 or index >= 9:
    send_to_webhook(webhook_url, "", username=username, attachments=attachments[index:])

def export_comparison(webhook_url, extension_id, comparison, old_version, new_version, deobfuscation_time):
  manifest = extensions.read_manifest(extension_id)

  changed_list = []
  for filename in comparison["changed"]:
    changed_list.append(f" - {filename}")
  changed_str = "\n".join(changed_list)

  attachments = []
  for filename, diff in comparison["changed"].items():
    attachments.append((filename.replace("/", "_")+".diff", diff))

  update_notif_data = {
    "extension_name": manifest["name"], 
    "old_version": old_version,
    "new_version": new_version,
    "changed_list": changed_str,
    "extension_id": extension_id,
    "deobfuscation_time": deobfuscation_time
  }
  update_notif = utils.get_template("update_notif.md").format(**update_notif_data)

  #todo: refactor to avoid duplicated code
  if comparison["created"]:
    created_list = []
    for filename in comparison["created"]:
      created_list.append(f" - {filename}")
    created_str = "\n".join(created_list)

    for filename, diff in comparison["created"].items():
      attachments.append((filename.replace("/", "_")+".diff", diff))
    update_notif += utils.get_template("new_files.md").format(new_files=created_str)
  
  if comparison["deleted"]:
    deleted_list = []
    for filename in comparison["deleted"]:
      deleted_list.append(f" - {filename}")
    deleted_str = "\n".join(deleted_list)

    for filename, diff in comparison["deleted"].items():
      attachments.append((filename.replace("/", "_")+".diff", diff))
    update_notif += utils.get_template("deleted_files.md").format(deleted_files=deleted_str)

  send_to_webhook(webhook_url, update_notif, attachments=attachments)