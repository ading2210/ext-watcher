from modules import updates, crx, deobfuscate
import time

extension_id = "haldlgldplgnggkjaafhelgiaglafanh"
update_url_base = "https://ext.goguardian.com/stable.xml"

print("Downloading extension...")
version, crx_data = updates.download_crx(extension_id, base=update_url_base)

print("Extracting extension...")
extracted_path = f"cache/{extension_id}/{version}"
crx.extract_crx(crx_data, extracted_path)

print("Deobfuscating extension source...")
start = time.time()
deobfuscate.process_directory(extracted_path)
end = time.time()

print(f"Deobfuscation took {round(end-start, 2)} seconds.")