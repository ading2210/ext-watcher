from modules import updates, crx, deobfuscate, utils

import time
import pathlib
import json
import logging

#define paths
base_path = pathlib.Path(__file__).resolve().parent
extensions_dir = base_path / "extensions"
config_dir = base_path / "config"
default_config_path = config_dir / "default.json"
config_path = config_dir / "config.json"

#read config
if not config_path.exists():
  config_path.write_text(default_config_path.read_text())
  raise FileNotFoundError("config/config.json needs to be modified")
config = json.loads(config_path.read_text())

#setup logger
utils.logger.setLevel(logging.DEBUG)

#main program
logging.info(f"Checking updates for {len(config['watched_extensions'])} extensions...")
for extension_id, options in config["watched_extensions"].items():
  logging.info(f"Processing extension {extension_id}...")
  extension_dir = extensions_dir / extension_id
  update_url = options.get("update_url")

  if not extension_dir.exists():
    logging.info(f"Extension is not cached. Downloading and extracting CRX for {extension_id}...")
    version, crx_data = updates.download_crx(extension_id, base=update_url)
    crx.extract_crx(crx_data, extension_dir / version)
    logging.info(f"Deobfuscating extension {extension_id}. This may take a while.")
    deobfuscate.process_directory(extension_dir / version)
    logging.info(f"Done deobfuscating {extension_id}.")
    continue

  available_versions = [str(subdir.relative_to(extension_dir)) for subdir in extension_dir.iterdir()]
  logging.debug(available_versions)

'''
extension_id = "haldlgldplgnggkjaafhelgiaglafanh"
update_url_base = "https://ext.goguardian.com/stable.xml"

print("Downloading extension...")
version, crx_data = updates.download_crx(extension_id, base=update_url_base)
#with open("/tmp/extension-m-3.0.6431.1-stable-crx2.crx", "rb") as f:
#  crx_data = f.read()
#version = "3.0.6431.1"

print("Extracting extension...")
extracted_path = f"cache/{extension_id}/{version}"
crx.extract_crx(crx_data, extracted_path)

print("Deobfuscating extension source...")
start = time.time()
deobfuscate.process_directory(extracted_path)
end = time.time()

print(f"Deobfuscation took {round(end-start, 2)} seconds.")
'''