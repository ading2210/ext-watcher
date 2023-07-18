#discord webhook wrapper

from modules import extensions, utils

import requests
import json

config = utils.config

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

def format_file_list(file_list):
  formatted_list = []
  for filename in file_list:
    formatted_list.append(f" - {filename}")
  return "\n".join(formatted_list)

def format_diffs(diffs_dict, name):
  if config["collapse_diffs"]:
    return [[name + ".diff", "\n\n".join(diffs_dict.values())]]
  
  attachments = []
  for filename, diff in diffs_dict.items():
    attachments.append((filename.replace("/", "_")+".diff", diff))
  return attachments

def export_comparison(webhook_url, extension_id, comparison, old_version, new_version, deobfuscation_time):
  manifest = extensions.read_manifest(extension_id)

  changed_str = format_file_list(comparison["changed"])
  attachments = format_diffs(comparison["changed"], "changed")

  update_notif_data = {
    "extension_name": manifest["name"], 
    "old_version": old_version,
    "new_version": new_version,
    "changed_list": changed_str,
    "extension_id": extension_id,
    "deobfuscation_time": deobfuscation_time
  }
  update_notif = utils.get_template("update_notif.md").format(**update_notif_data)

  if comparison["created"]:
    created_str = format_file_list(comparison["created"])
    attachments += format_diffs(comparison["created"], "created")
    update_notif += utils.get_template("new_files.md").format(new_files=created_str)
  
  if comparison["deleted"]:
    deleted_str = format_file_list(comparison["deleted"])
    attachments += format_diffs(comparison["deleted"], "deleted")
    update_notif += utils.get_template("deleted_files.md").format(deleted_files=deleted_str)

  send_to_webhook(webhook_url, update_notif, attachments=attachments)