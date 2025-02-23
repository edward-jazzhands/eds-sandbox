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
# The optimized URLs are saved to a file called {dir_path_str}.txt (folder containing 
# the images) in the same directory as this script.


from typing import Dict
from pathlib import Path
from rich.progress import track
from rich.progress import Progress
from rich.console import Console
console = Console()

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
console.log("[green]Files in the directory:[/green]")
for key, value in files.items():
    console.log(f"[yellow]{key}[/yellow] : {value}")


#########################
#~   Upload Pictures   ~#
#########################

secure_urls = {}
for key in track(files, description="Uploading images..."):
    path = files[key]
    upload_result: Dict = cloudinary.uploader.upload(
        path,
        public_id = key,
        asset_folder = dir_path_str,
        use_asset_folder_as_public_id_prefix = True
    )
    fixed_public_id = upload_result["public_id"] # returns the public id with the asset folder prefix
    secure_urls[fixed_public_id] = upload_result["secure_url"]


optimized_urls = {}
for key in secure_urls.keys():
    optimize_url, _ = cloudinary_url(key, fetch_format="auto", quality="auto")
    optimized_urls[key] = optimize_url

# print the optimized urls to a file
console.log("[green]Optimized URLs:[/green]")
with open(f"{dir_path_str}.txt", "w") as f:
    for key, value in optimized_urls.items():
        f.write(f"{key}: {value}\n")
        console.log(f"[yellow]{key}[/yellow] : {value}")

console.log(f"[green]Optimized URLs saved to [cyan]{dir_path_str}.txt")
