import os
import shutil
from generate import copy_files, generate_pages

from textnode import TextNode

static_path = "./static"
content_path = "./content"
public_path = "./public"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    print("Copying static files to public directory...")
    copy_files(static_path, public_path)
    generate_pages(content_path, template_path, public_path)
main()
