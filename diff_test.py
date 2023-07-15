from modules import compare
import time

print("Generating diffs...")
start = time.time()
compare_result = compare.compare_directory("cache/haldlgldplgnggkjaafhelgiaglafanh/3.0.6431.1", "cache/haldlgldplgnggkjaafhelgiaglafanh/3.0.6692.1")
end = time.time()
print(f"Generating diffs took {round(end-start, 2)} seconds.")