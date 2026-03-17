import re
from textnode import TextNode,TextType, split_nodes_delimiter,text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
import os
import shutil

from block import BlockType, block_to_block
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

def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        html_node = block_to_HTML_node(block)
        block_nodes.append(html_node)
    return ParentNode("div",block_nodes)


def block_to_HTML_node(block):
    block_type = block_to_block(block)
    if block_type == BlockType.PARAGRAPH:
        block = block.replace("\n"," ")
        return ParentNode("p",text_to_children(block))
    elif block_type == BlockType.HEADING:
        val, text = handle_headings(block)
        return ParentNode(f"h{val}",text_to_children(text))
    elif block_type == BlockType.QUOTE:
        block = handle_quotes(block)
        return ParentNode(f"blockquote",text_to_children(block))
    elif block_type == BlockType.Or_List:
        parents = handle_lists(block)
        return ParentNode("ol",parents)
    elif block_type == BlockType.Un_List:
        parents = handle_lists(block)
        return ParentNode("ul",parents)
    elif block_type == BlockType.CODE:
        block = block.removeprefix("```")
        block = block.removesuffix("```")
        block = block.lstrip("\n")
        code_block = TextNode(block,TextType.CODE)
        child = text_node_to_html_node(code_block)
        return ParentNode("pre",[child])
    
    
def text_to_children(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def handle_lists(block):
    block_type = block_to_block(block)
    new_list = block.split("\n")
    if block_type == BlockType.Or_List:
        new_list = [line.split(". ",1)[1] for line in new_list]
    elif block_type == BlockType.Un_List:
        new_list = [z.removeprefix("- ") for z in new_list]
    parents = []
    for children in new_list:
        child = (text_to_children(children))
        parent = ParentNode("li",child)
        parents.append(parent)
    return parents

def handle_headings(block):
    if block.startswith("# "):
        val = 1
        text = block.removeprefix("# ")
    elif block.startswith("## "):
        val = 2
        text = block.removeprefix("## ")
    elif block.startswith("### "):
        val = 3
        text = block.removeprefix("### ")
    elif block.startswith("#### "):
        val = 4
        text = block.removeprefix("#### ")
    elif block.startswith("##### "):
        val = 5
        text = block.removeprefix("##### ")      
    elif block.startswith("###### "):
        val = 6
        text = block.removeprefix("###### ")
    return val,text

def handle_quotes(block):
    new_list = block.split("\n")
    new_list = [line.removeprefix("> ") for line in new_list ]
    return " ".join(new_list)

def copy_source_to_destination(src,dst):
    dir = os.listdir(src)
    if not os.path.exists(src):
        raise Exception(f"Path: {src} not found")
    if not os.path.exists(dst):
        raise Exception(f"Path: {dst} not found")
    print(f"Deleting {dst} ")
    shutil.rmtree(dst)

    if not os.path.isfile(dst):
        os.mkdir(dst)

    print(f"Copying {src} to {dst}")
    shutil.copy(dir[0])
    copy_source_to_destination(dir[1:])