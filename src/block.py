
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    Un_List = "unordered_list"
    Or_List = "ordered_list"

def block_to_block(block):
    if block.startswith("```"):
        return BlockType.CODE
    elif block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.HEADING
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.Un_List
    elif block.startswith("1. "):
        return BlockType.Or_List
    else:
        return BlockType.PARAGRAPH