import os
import re
from pathlib import Path

root_dir = Path('/Users/cozuna/Documents/WebSites/ozuna printing')
images_dir = root_dir / 'assets' / 'images'

# Collect all HTML and CSS files
html_files = list(root_dir.rglob('*.html'))
css_files = list(root_dir.rglob('*.css'))
all_files = html_files + css_files

# Regex to match image names with resolution suffixes, e.g., -300x197.jpg
# We match the part before the suffix, the suffix, and the extension
res_suffix_pattern = re.compile(r'(-\d+x\d+)(\.[a-zA-Z0-9]+)$')

print("Step 1: Normalizing image references in HTML/CSS to point to high-res originals...")
modified_files = 0
for filepath in all_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        continue

    # We need to find all references to /assets/images/...
    # Then see if they end with -WxH.ext
    # A simple string replace won't work perfectly unless we parse.
    # But we can find all matches of /assets/images/([\w\-\.]+)\b
    def replace_image_url(match):
        filename = match.group(1)
        res_match = res_suffix_pattern.search(filename)
        if res_match:
            base_filename = filename[:res_match.start()] + res_match.group(2)
            # Check if base_filename exists
            if (images_dir / base_filename).exists():
                return f"/assets/images/{base_filename}"
        return match.group(0) # Unmodified

    # Use regex to find /assets/images/something.ext
    # and replace if it has a resolution suffix and the base file exists.
    new_content = re.sub(r'/assets/images/([\w\-\.]+)', replace_image_url, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified_files += 1

print(f"Updated image references in {modified_files} files.")

print("Step 2: Identifying all USED images...")
used_images = set()

# Parse all files again to find all used images
for filepath in all_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        continue
        
    matches = re.findall(r'/assets/images/([\w\-\.]+)', content)
    for m in matches:
        used_images.add(m)

print(f"Found {len(used_images)} unique images referenced in the code.")

print("Step 3: Deleting UNUSED images...")
deleted_count = 0
for img_file in images_dir.glob('*'):
    if img_file.is_file():
        if img_file.name not in used_images:
            # Maybe it's referenced url-encoded? Unlikely for these filenames.
            print(f"  Deleting unused image: {img_file.name}")
            img_file.unlink()
            deleted_count += 1

print(f"Deleted {deleted_count} unused image files.")
print("Cleanup complete.")
