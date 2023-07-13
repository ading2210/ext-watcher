from modules import updates, crx, deobfuscate

extension_id = "iheobagjkfklnlikgihanlhcddjoihkg"

crx_data = updates.download_crx(extension_id)
crx.extract_crx(crx_data, f"cache/{extension_id}")

deobfuscate.process_directory(f"cache/{extension_id}")