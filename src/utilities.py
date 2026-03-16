import re
from textnode import TextNode,TextType, split_nodes_delimiter
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_images(old_node.text)
        working_text = old_node.text
        if not matches:
            new_node = TextNode(working_text,TextType.TEXT)
            new_nodes.append(new_node)
        else:
            for alt,url in matches:
                text = working_text.split(f"![{alt}]({url})",1)
                if text[0] == "":
                    pass # Dont add
                else:
                    new_node = TextNode(text[0],TextType.TEXT)
                    new_nodes.append(new_node)

                working_text = text[1]
                new_node = TextNode(alt,TextType.IMAGES,url)
                new_nodes.append(new_node)
            if working_text != "":
                new_node = TextNode(working_text,TextType.TEXT)
                new_nodes.append(new_node)
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_links(old_node.text)
        working_text = old_node.text
        if not matches:
            new_node = TextNode(working_text,TextType.TEXT)
            new_nodes.append(new_node)
        else:
            for alt,url in matches:
                text = working_text.split(f"[{alt}]({url})",1)
                if text[0] == "":
                    pass # Dont add
                else:
                    new_node = TextNode(text[0],TextType.TEXT)
                    new_nodes.append(new_node)

                working_text = text[1]
                new_node = TextNode(alt,TextType.LINKS,url)
                new_nodes.append(new_node)
            if working_text != "":
                new_node = TextNode(working_text,TextType.TEXT)
                new_nodes.append(new_node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
    nodes = (split_nodes_delimiter(nodes,"**",TextType.BOLD))
    nodes = (split_nodes_delimiter(nodes,"_",TextType.ITALIC))
    nodes = (split_nodes_images(nodes))
    nodes = (split_nodes_link(nodes))
    return nodes


def markdown_to_blocks(markdown):
    text = markdown.split("\n\n")
    new_text = []
    for item in text:
        strip_1 = item.strip()
        if item == "":
            continue
        else:
            new_text.append(strip_1)
    return new_text