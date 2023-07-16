#handle the stored extensions

from modules import updates
import pathlib

base_path = pathlib.Path(__file__).resolve().parent.parent
extensions_path = base_path / "extensions"

def get_newest_cached_version(extension_id):
  extension_dir = extensions_path / extension_id
  available_versions = [str(subdir.relative_to(extension_dir)) for subdir in extension_dir.iterdir()]
  newest_cached_version = updates.max_version(available_versions)
  return newest_cached_version

def get_extension_dir(extension_id):
  newest_version = get_newest_cached_version(extension_id)
  return extensions_path / extension_id / newest_version

def read_manifest(extension_id):
  extension_dir = get_extension_dir(extension_id)
  manifest_path = extension_dir / "manifest.json"
  manifest_string = manifest_path.read_text()
  return json.loads(manifest_string)