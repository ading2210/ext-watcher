#interfaces with google's extension update api

import requests
import urllib
import re

chrome_version = "114.0.5735.198"
update_url_base = "https://clients2.google.com/service/update2/crx"
update_params = "?response=redirect&os=cros&arch=x86-64&os_arch=x86-64&nacl_arch=x86-64&prod=chromiumcrx&prodchannel=unknown&prodversion={chrome_version}&acceptformat=crx2,crx3&x=id%3D{extension_id}%26uc"

def get_update_url(extension_id):
  params = update_params.format(chrome_version=chrome_version, extension_id=extension_id)
  url = update_url_base + params
  return url

def get_current_version(extension_id):
  url = get_update_url(extension_id)
  r = requests.get(url, allow_redirects=False)
  r.raise_for_status()
  redirect = r.headers["Location"]

  version = re.findall(r"extension_(.+)?\.crx", redirect)[0]
  version = version.replace("_", ".")
  return version