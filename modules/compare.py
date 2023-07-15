#compare two extension versions and create a diff

import difflib
import filecmp
import pathlib

def check_utf8(file_path):
  try:
    with open(file_path, "r") as f:
      f.read()
    return True
  except UnicodeDecodeError:
    return False 

def generate_diff(old_text, new_text, old_filename, new_filename):
  old_split = old_text.split("\n")
  new_split = new_text.split("\n")

  diff_gen = difflib.unified_diff(old_split, new_split, fromfile=old_filename, tofile=new_filename)
  diff_text = "\n".join(diff_gen)

  return diff_text

def generate_diff_from_file(old_file, new_file):
  old_text = ""
  if old_file:
    old_text = old_file.read_text()
  
  new_text = ""
  if new_file:
    new_text = new_file.read_text()

  return generate_diff(old_text, new_text, str(old_file), str(new_file))

#returns list of strings matching the query
def walk_comparison_subdirs(comparison, query, base_path="", enforce_blacklist=True):
  relative_items = getattr(comparison, query)
  
  absolute_items = []
  for item in relative_items:
    item_path = base_path + "/" + item
    absolute_items.append(item_path)

  for subdir, subdir_comparison in comparison.subdirs.items():
    path = base_path
    path = base_path + "/" + subdir
    absolute_items += walk_comparison_subdirs(subdir_comparison, query, base_path=path)
  
  #remove leading /
  if base_path == "":
    filtered_items = []
    for item in absolute_items:
      if item.startswith("/"):
        item = item.replace("/", "", 1)
      filtered_items.append(item)
    return filtered_items

  return absolute_items

def generate_diff_safe(old_file, new_file):
  if old_file and not old_file.is_file():
    return generate_diff("[Cannot generate diff: old target is a directory]", "", str(old_file), str(new_file))
  if new_file and not new_file.is_file():
    return generate_diff("[Cannot generate diff: new target is a directory]", "", str(old_file), str(new_file))
  
  if old_file and not check_utf8(old_file):
    return generate_diff("[Cannot generate diff: old file does not contain text]", "", str(old_file), str(new_file))
  if new_file and not check_utf8(new_file):
    return generate_diff("[Cannot generate diff: new file does not contain text]", "", str(old_file), str(new_file))

  return generate_diff_from_file(old_file, new_file)

def compare_directory(old_dir, new_dir):
  old_dir = pathlib.Path(old_dir)
  new_dir = pathlib.Path(new_dir)
  comparison = filecmp.dircmp(old_dir, new_dir)

  changed_diffs = {}
  for diff_file in walk_comparison_subdirs(comparison, "diff_files"):
    changed_diffs[diff_file] = generate_diff_safe(old_dir/diff_file, new_dir/diff_file)

  deleted_diffs = {}
  for deleted_file in walk_comparison_subdirs(comparison, "left_only"):
    deleted_path = old_dir/deleted_file #is path object, not string
    deleted_items = [deleted_path]
    if deleted_path.is_dir():
      deleted_items += deleted_path.rglob("*")
    
    for deleted_item in deleted_items:
      relative_path_str = deleted_item.relative_to(old_dir)
      deleted_diffs[relative_path_str] = generate_diff_safe(deleted_item, None)
  
  created_diffs = {}
  for created_file in walk_comparison_subdirs(comparison, "right_only"):
    created_diffs[created_file] = generate_diff_from_file(None, new_dir/created_file)
  
  return {
    "changed": changed_diffs,
    "deleted": deleted_diffs,
    "created": created_diffs
  }