#wrapper for webcrack cli
#webcrack: https://github.com/j4k0xb/webcrack

import subprocess
import shutil
import io
import pathlib

webcrack_path = shutil.which("webcrack")
if not webcrack_path:
  raise FileNotFoundError("Webcrack is not installed, or it is not in your PATH.")

#call webcrack to deobfuscate a js file
def process_file(js_string):
  child = subprocess.Popen([webcrack_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out = child.communicate(input=js_string.encode())
  return out[0].decode()

#recursively deobfuscate a directory
#this will overwrite the files that are processed
def process_directory(dir_path):
  path = pathlib.Path(dir_path)
  for item in path.rglob("*"):
    if not item.is_file(): 
      continue
    if not item.suffix == ".js":
      continue
    
    js_string = item.read_text()
    processed_string = process_file(js_string)
    item.write_text(processed_string)

    if item.suffixes == [".min", ".js"]:
      item.rename(item.with_suffix("").with_suffix(".js"))