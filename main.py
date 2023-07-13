from modules import updates, crx, deobfuscate

extension_id = "cjpalhdlnbpafiamejdnhcphjbkeiagm"

crx_data = updates.download_crx(extension_id)
crx.extract_crx(crx_data, f"cache/{extension_id}")

with open(f"cache/{extension_id}/js/assets.js") as f:
  js_string = f.read()
  deobbed = deobfuscate.process_file(js_string)
  print(deobbed)