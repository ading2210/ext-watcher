from modules import webhook
import sys

with open("cache/diff/changed/manifest.json.diff") as f:
  diff_content = f.read()

attachments = {
  "manifest.json.diff": diff_content
}

webhook.send_to_webhook(sys.argv[1], "test content", attachments=attachments)