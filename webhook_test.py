from modules import webhook
import sys
import pathlib

attachments = []
diffs_path = pathlib.Path("cache/diff/changed/")
for item in diffs_path.rglob("*"):
  filename = str(item.relative_to(diffs_path))
  attachments.append((filename, item.read_bytes()))

webhook.send_to_webhook(sys.argv[1], "test content", attachments=attachments)