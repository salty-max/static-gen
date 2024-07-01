import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        sub_nodes = node.text.split(delimiter)
        if len(sub_nodes) % 2 == 0:
            raise ValueError("Invalid markdown: unmatched delimiter found")
        for i, part in enumerate(sub_nodes):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, text_type_text))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_image:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for image in images:
            if f"![{image[0]}]({image[1]})" in remaining_text:
                pre_image, remaining_text = remaining_text.split(f"![{image[0]}]({image[1]})")
                if pre_image:
                    new_nodes.append(TextNode(pre_image, text_type_text))
                new_nodes.append(TextNode(image[0], text_type_image, image[1]))
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_link:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for link in links:
            if f"[{link[0]}]({link[1]})" in remaining_text:
                pre_link, remaining_text = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
                if pre_link:
                    new_nodes.append(TextNode(pre_link, text_type_text))
                new_nodes.append(TextNode(link[0], text_type_link, link[1]))
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, text_type_text))
    return new_nodes


def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches
