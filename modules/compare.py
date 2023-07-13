#compare two extension versions and create a diff

import difflib
import filecmp

suffix_whitelist = [".txt", ".js", ".css", ".html", ".json"]

def generate_diff(old_text, new_text, filename):
  old_split = old_text.split("\n")
  new_split = new_text.split("\n")

  diff_gen = difflib.unified_diff(old_split, new_split, fromfile=filename, tofile=filename)
  diff_text = "\n".join(diff_gen)

  return diff_text

def compare_directory(old_dir, new_dir):
  comparison = filecmp.dircmp(old_dir, new_dir)
  return comparison.report_full_closure()