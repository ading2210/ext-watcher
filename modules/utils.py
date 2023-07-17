#random utils

import logging
import pathlib

logging.basicConfig()
logger = logging.getLogger()

base_dir = pathlib.Path(__file__).resolve().parent.parent

def check_utf8(file_path):
  try:
    with open(file_path, "r") as f:
      f.read()
    return True
  except UnicodeDecodeError:
    return False 

def load_template(template_name):
  template_path = base_dir / "templates" / template_name
  return template_path.read_text()