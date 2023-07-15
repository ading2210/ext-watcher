from modules import updates, crx, deobfuscate
import time
import pathlib
import json

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

if __name__ == "__main__":
  pass

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