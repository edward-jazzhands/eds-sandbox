# Cloudinary uploader script
# By Edward Jazzhands
# ----------------------------
# This script uploads images from a directory to Cloudinary,
# then returns a list of optimized URLs for the images.
# Intended Usage:
# 1. Have a folder containing images you want to upload.
# 2. Place this file beside that directory (not inside it, just next to it).
# 3. Run this script.
# 4. Enter the directory path when prompted.

# The script will upload the images to Cloudinary, then return a list of optimized URLs.
# The optimized URLs are saved to a file called "optimized_urls.txt" in the same directory as the images.


from typing import Dict
from pathlib import Path
from rich.progress import track

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

###################################
#~ Cloudinary API key and config ~#
###################################

cloudinary.logger.setLevel("DEBUG")

try:
    with open("cloudinary_api_secret.txt", "r") as f:
        api_secret = f.read().strip()
except FileNotFoundError:
    raise FileNotFoundError("cloudinary_api_secret.txt file not found.")
except:
    raise Exception("Error reading cloudinary_api_secret.txt file.")

# Configuration       
cloudinary.config( 
    cloud_name = "duftwfvqo", 
    api_key = "236645894295833", 
    api_secret = api_secret,
    secure=True
)

##################################
#~    Get Pictures to Upload    ~#
##################################


dir_path_str = input("Enter the directory path: ")
try:
    directory_path = Path(dir_path_str)
except:
    raise FileNotFoundError(f"Directory {dir_path_str} does not exist.")

files = {f.stem: f for f in directory_path.iterdir() if f.is_file()}
print("Files in the directory:")
for key, value in files.items():
    print(key, ":", value)


#########################
#~   Upload Pictures   ~#
#########################


secure_urls = {}
for key in track(files, description="Uploading images..."):
    value = files[key]
    upload_result: Dict = cloudinary.uploader.upload(
        value,
        public_id = key,
        asset_folder = dir_path_str,
        use_asset_folder_as_public_id_prefix = True
    )
    secure_urls[key] = upload_result["secure_url"]


optimized_urls = {}
for key in track(secure_urls, description="Optimizing images..."):
    value = secure_urls[key]
    optimize_url, _ = cloudinary_url(key, fetch_format="auto", quality="auto")
    optimized_urls[key] = optimize_url


# print the optimized urls to a file inside the original directory_path
with open(directory_path / "optimized_urls.txt", "w") as f:
    for key, value in optimized_urls.items():
        f.write(f"{key}: {value}\n")
