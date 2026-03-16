
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"

class TextNode():
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception(f"TextType: {text_node.text_type} not valid")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINKS:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGES:
            return LeafNode("img","",{"src": text_node.url,
                                      "alt": text_node.text })
        
def split_nodes_delimiter(old_nodes,delimiter,text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text.split(delimiter)
        if len(text) % 2 == 0:
            raise Exception(f"Closing delimiter for {delimiter} not found. Check text.")
        for i in range(0,len(text)):
            if i % 2 != 0:
                incoming_node = TextNode(text[i],text_type)
                new_nodes.append(incoming_node)
            elif text[i] == "":
                continue # Do nothing
            else:
                incoming_node = TextNode(text[i],TextType.TEXT)
                new_nodes.append(incoming_node)    
    return new_nodes
        