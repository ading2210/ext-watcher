#compare two extension versions and create a diff

from modules import utils

import difflib
import filecmp
import pathlib
import os

def generate_diff(old_text, new_text, old_filename, new_filename):
  old_split = old_text.split("\n")
  new_split = new_text.split("\n")

  diff_gen = difflib.unified_diff(old_split, new_split, fromfile=old_filename, tofile=new_filename, lineterm="")
  diff_text = "\n".join(diff_gen)

  return diff_text

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

def generate_diff_safe(old_file, new_file, base_str):
  old_path = str(old_file).replace(base_str, "", 1)
  new_path = str(new_file).replace(base_str, "", 1)
  if old_path.startswith("/"): 
    old_path = "." + old_path
  if new_path.startswith("/"):
    new_path = "." + new_path

  if old_file and not old_file.is_file():
    return generate_diff("[Cannot generate diff: old target is a directory]", "", old_path, new_path)
  if new_file and not new_file.is_file():
    return generate_diff("[Cannot generate diff: new target is a directory]", "", old_path, new_path)
  
  if old_file and not utils.check_utf8(old_file):
    return generate_diff("[Cannot generate diff: old file does not contain text]", "", old_path, new_path)
  if new_file and not utils.check_utf8(new_file):
    return generate_diff("[Cannot generate diff: new file does not contain text]", "", old_path, new_path)
  
  old_text = ""
  new_text = ""
  if old_file:
    old_text = old_file.read_text()
  if new_file:
    new_text = new_file.read_text()

  return generate_diff(old_text, new_text, old_path, new_path)

def compare_directory(old_dir, new_dir):
  old_dir = pathlib.Path(old_dir)
  new_dir = pathlib.Path(new_dir)
  base_str = os.path.commonpath([old_dir, new_dir])
  comparison = filecmp.dircmp(old_dir, new_dir)

  changed_diffs = {}
  for diff_file in walk_comparison_subdirs(comparison, "diff_files"):
    changed_diffs[diff_file] = generate_diff_safe(old_dir/diff_file, new_dir/diff_file, base_str)

  deleted_diffs = {}
  for deleted_file in walk_comparison_subdirs(comparison, "left_only"):
    deleted_path = old_dir/deleted_file #is path object, not string
    deleted_items = [deleted_path]
    if deleted_path.is_dir():
      deleted_items += deleted_path.rglob("*")
    
    for deleted_item in deleted_items:
      relative_path_str = str(deleted_item.relative_to(old_dir))
      deleted_diffs[relative_path_str] = generate_diff_safe(deleted_item, None, base_str)
  
  created_diffs = {}
  for created_file in walk_comparison_subdirs(comparison, "right_only"):
    created_diffs[created_file] = generate_diff_safe(None, new_dir/created_file, base_str)
  
  return {
    "changed": changed_diffs,
    "deleted": deleted_diffs,
    "created": created_diffs
  }