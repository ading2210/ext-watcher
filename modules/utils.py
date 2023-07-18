#random utils

import logging
import pathlib
import json

logging.basicConfig()
logger = logging.getLogger()

#handle paths
base_dir = pathlib.Path(__file__).resolve().parent.parent
extensions_dir = base_dir / "extensions"
config_dir = base_dir / "config"
default_config_path = config_dir / "default.json"
config_path = config_dir / "config.json"

#read config
if not config_path.exists():
  config_path.write_text(default_config_path.read_text())
  raise FileNotFoundError("config/config.json needs to be modified")
config = json.loads(config_path.read_text())

def check_utf8(file_path):
  try:
    with open(file_path, "r") as f:
      f.read()
    return True
  except UnicodeDecodeError:
    return False 

def get_template(template_name):
  template_path = base_dir / "templates" / template_name
  return template_path.read_text()