#random utils

import logging

logging.basicConfig()
logger = logging.getLogger()

def check_utf8(file_path):
  try:
    with open(file_path, "r") as f:
      f.read()
    return True
  except UnicodeDecodeError:
    return False 