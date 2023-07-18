from modules import updates, crx, deobfuscate, utils, extensions, webhook, compare

import time
import pathlib
import json
import logging

config = utils.config

#setup logger
utils.logger.setLevel(logging.INFO)
if config["debug"]:
  utils.logger.setLevel(logging.DEBUG)

#main program loop
utils.logger.info(f"Checking updates for {len(config['watched_extensions'])} extensions...")
for extension_id, options in config["watched_extensions"].items():
  utils.logger.info(f"Processing extension {extension_id}...")
  extension_dir = utils.extensions_dir / extension_id
  update_url = options.get("update_url") or updates.update_url_base

  update_needed = True
  if extension_dir.exists():
    utils.logger.info(f"Checking updates for {extension_id}...")
    newest_cached_version = extensions.get_newest_cached_version(extension_id)
    update_needed = updates.check_update(extension_id, newest_cached_version, base=update_url)

  if not update_needed:
    utils.logger.info(f"Update is not available for {extension_id}.")
  else:
    utils.logger.info(f"Update is available. Downloading and extracting CRX for {extension_id}...")
    old_version = extensions.get_newest_cached_version(extension_id)
    version, crx_data = updates.download_crx(extension_id, base=update_url)
    crx.extract_crx(crx_data, extension_dir / version)

    start = time.time()
    utils.logger.info(f"Deobfuscating extension {extension_id}. This may take a while.")
    deobfuscate.process_directory(extension_dir / version)
    end = time.time()
    deobfuscation_time = round(end-start, 2)
    utils.logger.info(f"Deobfuscation took {deobfuscation_time} seconds.")

  if update_needed and old_version:
    utils.logger.info(f"Sending notification to webhook...")
    comparison = compare.compare_directory(extension_dir / old_version, extension_dir / version)
    for webhook in config["discord_webhooks"]:
      webhook.export_comparison(webhook, extension_id, comparison, old_version, version, deobfuscation_time)


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