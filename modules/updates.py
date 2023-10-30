#interfaces with google's extension update api

import requests
import urllib
import re
from packaging import version
from lxml import etree

chrome_version = "114.0.5735.198"
update_url_base = "https://clients2.google.com/service/update2/crx"
update_params = "?response=redirect&os=cros&arch=x86-64&os_arch=x86-64&nacl_arch=x86-64&prod=chromiumcrx&prodchannel=unknown&prodversion={chrome_version}&acceptformat=crx2,crx3&x=id%3D{extension_id}%26uc"

def max_version(versions):
  return max(versions, key=version.parse)

def get_update_url(extension_id, base=update_url_base):
  params = update_params.format(chrome_version=chrome_version, extension_id=extension_id)
  url = base + params
  
  return url

def parse_updatecheck_xml(xml_string, extension_id):
  root = etree.fromstring(xml_string.encode())
  for app in root.iterchildren():
    if app.get("appid") == extension_id:
      updatecheck = app.getchildren()[0]
      redirect = updatecheck.get("codebase")
      version = updatecheck.get("version")
      return redirect, version
      break
  else:
    raise KeyError("Could not find the download URL.")

def get_current_version(extension_id, base=update_url_base):
  url = get_update_url(extension_id, base)
  r = requests.head(url)
  r.raise_for_status()
  
  if r.headers["Content-Type"].startswith("text/xml"):
    r2 = requests.get(url)
    redirect, version = parse_updatecheck_xml(r2.text, extension_id)

  else:
    redirect = r.headers["Location"]
    print(redirect)
    version = re.findall(r"[A-Z]{32}_(.+)?\.crx", redirect)[0]
    version = version.replace("_", ".")
  
  return version

def check_update(extension_id, current_version, base=update_url_base):
  latest = get_current_version(extension_id, base)
  latest_parsed = version.parse(latest)
  current_parsed = version.parse(current_version)
  
  return latest_parsed > current_parsed

def download_crx(extension_id, output=None, base=update_url_base):
  url = get_update_url(extension_id, base)
  r = requests.get(url)
  r.raise_for_status()

  if r.headers["Content-Type"].startswith("text/xml"):
    redirect, version = parse_updatecheck_xml(r.text, extension_id)
    r = requests.get(redirect)
  else:
    version = get_current_version(extension_id)

  crx_data = r.content
  if output:
    with open(output, "wb") as f:
      f.write(crx_data)

  return version, crx_data