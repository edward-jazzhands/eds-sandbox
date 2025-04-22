import requests
import re
import os
import sys
from pathlib import Path
import yaml
import datetime
from markdown_it import MarkdownIt

from rich.console import Console
console = Console()

console.print(f"[green]Starting time: {datetime.datetime.now()} \n")

DOWNLOAD_REPO_DATA_AFTER = False                #! Set to True to allow Stage 2.

# Load GitHub token from environment
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'} if token else {}

# NOTE: This script is using the Textual READM

url = 'https://github.com/Textualize/transcendent-textual/raw/refs/heads/main/README.md'
yaml_file_path = Path("misc/libraries.yml") 
readme_file_path = Path("misc/README.md")


class SpacedDumper(yaml.Dumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if self.indent == 0:            # Add a blank line between top-level entries
            super().write_line_break()

def download_file() -> requests.Response:

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()                     # Raises HTTPError for bad responses (4xx or 5xx)
        console.print("\n[yellow]Successfully fetched the README.md file. Next stage... \n") # only reached if no error is raised.
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error while fetching the URL: {url}. Error: {e}")
    except Exception as e:
        raise Exception(f"Error while fetching the URL: {url}. Error: {e}")
    else:
        return response

def parse_file(file_path: str) -> str:

    md = MarkdownIt()
    tokens = md.parse(open(file_path, "r").read())

    libraries = {}

    for t in tokens:
        if t.type == "heading_open":
            # console.print(t)
            pass

        if t.type == "inline":
            # console.print(t.children)
            # console.print("[red]-----------------------------------")
            for child in t.children:
                if child.type == "text":
                    if t.level == 1:
                        # console.print(f"[green]{child.content}")
                        libraries[child.content] = {}
                    else:
                        # console.print(f"  {child.content}")
                        pass
                if child.type == "link_open":
                    # console.print(child.attrs['href'])
                    pass
            continue
        
    # console.print(libraries)
    # #         console.print(t.level*" ", t.content)
    console.print(tokens[:50])


    # split1 = response.text.split("## Textualize libraries and tools")   # split at top section
    # split2 = split1[1].split("## Applications built with Textual")      # disregard top section, split at bottom section
    # split3 = split2[0].split("## Third-party libraries")                # disregard bottom section, split at middle

    # # split3 contains our 2 sections of interest:
    #     # split3[0] is official Textualize libraries and tools
    #     # split3[1] is third-party libraries

    # textualize_libraries = split3[0].strip().split("\n")
    # third_party_libraries = split3[1].strip().split("\n")

    # def normalize_line(line: str, dict_to_update: dict, official: bool) -> None:
    #     name = re.findall(r'\[(.*?)\]', line)[0]
    #     name = name.replace(" ", "-").lower()
    #     url  = re.findall(r'\((.*?)\)', line)[0]
    #     description = line.split(") - ")[1]
    #     # dict_to_update[name] = [url, description]
    #     dict_to_update[name] = {
    #         "url": url,
    #         "img": f"libraries/{name}.png",
    #         "description": description,
    #         "official": official
    #     }

    # textualize_libraries_dict = {}
    # for line in textualize_libraries:
    #     normalize_line(line, textualize_libraries_dict, True)

    # third_party_libraries_dict = {}
    # for line in third_party_libraries:
    #     normalize_line(line, third_party_libraries_dict, False)

    # libraries = {**textualize_libraries_dict, **third_party_libraries_dict}
    # return libraries


def stage_two(libraries: dict): 

    for name, lib_data in libraries.items():
        
        if 'github.com' not in lib_data['url']:            # Skip if not a GitHub repo
            continue
            
        path = lib_data['url'].replace('https://github.com/', '').strip('/')     # Extract owner/repo
        if not path:                   
            print(f"Malformed URL for {name}: {lib_data['url']}")
            continue

        try:
            response = requests.get(f'https://api.github.com/repos/{path}', headers=headers)   # Fetch repo data
            response.raise_for_status()
        except Exception as e:
            raise SystemExit(f"Error fetching data for {name}: {e}")
        else:  
            print(f"Fetch successful for {name}: {response.status_code}. Proceeding...")
            repo_data = response.json()

            if 'pushed_at' in repo_data:                            
                lib_data['pushed_at'] = repo_data['pushed_at']
            if 'stargazers_count' in repo_data:
                lib_data['stars'] = repo_data['stargazers_count']
            if 'owner' in repo_data:
                lib_data['author'] = repo_data['owner']['login']



if not readme_file_path.exists():               # Check if README.md file already exists
    response = download_file()                  # Download the README.md file
    with open(readme_file_path, 'w') as file:
        file.write(response.text)               # Save the content to a local file
else:
    console.print(f"[yellow]README.md already exists at {readme_file_path}. Skipping download.")

parse_file(readme_file_path)                    # Parse the file and extract libraries







# # Save updated data
# try:
#     with open(yaml_file_path, 'w') as file:
#         yaml.dump(libraries, file, Dumper=SpacedDumper, indent=2)
# except Exception as e:
#     raise SystemExit(f"Error writing to file: {e}")
# else:
#     print("File written successfully.")
#     print(f"Finished time: {datetime.datetime.now()} \n")   

# print("Skipping Stage 2. Exiting...")
# exit(0)



# # Save updated data
# try:
#     with open(yaml_file_path, 'w') as file:
#         yaml.dump(libraries, file, Dumper=SpacedDumper, indent=2)
# except Exception as e:
#     raise SystemExit(f"Error writing to file: {e}")
# else:
#     print("File written successfully.")
#     print(f"Finished time: {datetime.datetime.now()} \n")    