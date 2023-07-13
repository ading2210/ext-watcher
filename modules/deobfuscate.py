#wrapper for webcrack cli
#webcrack: https://github.com/j4k0xb/webcrack

import subprocess
import shutil
import io

webcrack_path = shutil.which("webcrack")
if not webcrack_path:
  raise FileNotFoundError("Webcrack is not installed, or it is not in your PATH.")

#call webcrack to deobfuscate js file
def process_file(js_string):
  child = subprocess.Popen([webcrack_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out = child.communicate(input=js_string.encode())
  return out[0].decode()