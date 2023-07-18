#handle the stored extensions

from modules import updates, utils
import pathlib
import json

extensions_path = utils.base_dir / "extensions"

def get_newest_cached_version(extension_id):
  extension_dir = extensions_path / extension_id
  if not extension_dir.exists():
    return None
  available_versions = [str(subdir.relative_to(extension_dir)) for subdir in extension_dir.iterdir()]
  newest_cached_version = updates.max_version(available_versions)
  return newest_cached_version

def get_base_extension_dir(extension_id):
  return extensions_path / extension_id

def get_extension_dir(extension_id):
  newest_version = get_newest_cached_version(extension_id)
  return get_base_extension_dir(extension_id) / newest_version

def read_manifest(extension_id):
  extension_dir = get_extension_dir(extension_id)
  manifest_path = extension_dir / "manifest.json"
  manifest_string = manifest_path.read_text()
  return json.loads(manifest_string)