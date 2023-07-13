#compare two extension versions and create a diff

import difflib
import filecmp
import pathlib

suffix_whitelist = [".txt", ".js", ".css", ".html", ".json"]

def generate_diff(old_text, new_text, old_filename, new_filename):
  old_split = old_text.split("\n")
  new_split = new_text.split("\n")

  diff_gen = difflib.unified_diff(old_split, new_split, fromfile=old_filename, tofile=new_filename)
  diff_text = "\n".join(diff_gen)

  return diff_text

def generate_diff_from_file(old_file=None, new_file=None):
  if old_file:
    old_text = old_file.read_text()
  else:
    old_text = ""
  
  if new_file:
    new_text = new_file.read_text()
  else:
    new_text = ""

  return generate_diff(old_text, new_text, str(old_file), str(new_file))

def walk_comparison_subdirs(comparison, query, base_path=""):
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

def compare_directory(old_dir, new_dir):
  old_dir = pathlib.Path(old_dir)
  new_dir = pathlib.Path(new_dir)
  comparison = filecmp.dircmp(old_dir, new_dir)

  print(walk_comparison_subdirs(comparison, "diff_files"))

  for diff_file in walk_comparison_subdirs(comparison, "diff_files"):
    print(old_dir/diff_file)
    generate_diff_from_file(old_dir/diff_file, new_dir/diff_file)