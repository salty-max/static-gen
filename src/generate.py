import os
import shutil
from block_markdown import markdown_to_html_node

def extract_title(md):
    lines = md.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise Exception("Invalid page: header is missing")

def generate_pages(content_dir_path, template_path, dest_dir_path):
    if not os.path.exists(content_dir_path):
        raise Exception("No such file or directory: {content_dir_path}")
    os.makedirs(dest_dir_path, exist_ok=True)
    for filename in os.listdir(content_dir_path):
        from_path = os.path.join(content_dir_path, filename)
        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, filename.replace(".md", ".html"))
                print(from_path, dest_path)
                generate_page(from_path, template_path, dest_path)
        else:
            nested_dest_path = os.path.join(dest_dir_path, filename)
            generate_pages(from_path, template_path, nested_dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as md_file:
        content = md_file.read()
    with open(template_path, 'r') as template_file:
        template = template_file.read()
    title = extract_title(content)
    node = markdown_to_html_node(content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", node.to_html())
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(template)

def copy_files(source_dir, target_dir):
    if not os.path.exists(source_dir):
        raise Exception(f"No such file or directory: {source_dir}")
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    for filename in os.listdir(source_dir):
        from_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(target_dir, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files(from_path, dest_path)

