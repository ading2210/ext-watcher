#handle the crx file format

import struct
import io
import zipfile

#convert crx to zip file
def convert_crx(crx_data):
  header_numbers = struct.unpack("<4sIII", crx_data[:16])
  magic, version, pubkey_length, signature_length = header_numbers
  
  if version == 2:
    zip_index = 16 + pubkey_length + signature_length
  else:
    zip_index = 12 + pubkey_length

  zip_data = crx_data[zip_index:]
  return zip_data

#extract a zip file
def extract_zip(zip_data, output_dir):
  input_file = io.BytesIO(zip_data)
  with zipfile.ZipFile(input_file, "r") as zip_ref:
    zip_ref.extractall(output_dir)

#convert and extract crx
def extract_crx(crx_data, output_dir):
  zip_data = convert_crx(crx_data)
  extract_zip(zip_data, output_dir)