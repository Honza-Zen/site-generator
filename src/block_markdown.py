from enum import Enum
from htmlnode import LeafNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE_BLOCK = "code_block"
    QUOTE = "quote"
    UNORDERED_LIST = "unodreder_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        new_blocks.append(block)
    return new_blocks


def block_to_block_type(md_block):
    if re.findall(r"^#{1,6} ", md_block):
        return BlockType.HEADING
    elif md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE_BLOCK
    elif md_block.startswith(">"):
        for line in md_block.split("\n"):
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    elif md_block.startswith("* ") or md_block.startswith("- "):
        for line in md_block.split("\n"):
            if not line.startswith("* ") and not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    elif md_block.startswith("1. "):
        i = 1
        for line in md_block.split("\n"):
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1 
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    


def markdown_to_html_node(markdown):
    
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match(block_type):
            case BlockType.HEADING:
                heading, text = get_heading_text(block)
                html_nodes.append(ParentNode(heading, text_to_children(text)))

            case BlockType.CODE_BLOCK:
                text = get_code_block_text(block)
                code_node = ParentNode("code", text_to_children(text))
                html_nodes.append(ParentNode("pre", [code_node]))

            case BlockType.QUOTE:
                text = get_quote_text(block)
                html_nodes.append(ParentNode("blockquote", text_to_children(text)))

            case BlockType.UNORDERED_LIST:
                text = get_unordered_list_text(block)
                html_nodes.append(ParentNode("ul", text))

            case BlockType.ORDERED_LIST:
                text = get_ordered_list_text(block)
                html_nodes.append(ParentNode("ol", text))

            case _:
                text = get_paragraph_text(block)
                html_nodes.append(ParentNode("p", text_to_children(text)))
            
    return ParentNode("div", html_nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def get_paragraph_text(text):
    lines = text.split("\n")
    return " ".join(lines)

def get_heading_text(md_text):
    hash_count = 0
    for i in md_text:
        if i == "#":
            hash_count += 1
    return f"h{hash_count}", md_text[hash_count+1:] #+1 is for the space

def get_ordered_list_text(text):
    block = text.split("\n")
    new_text = []
    for line in block:
        new_text.append(ParentNode("li", text_to_children(line[3:].strip())))
    return new_text

def get_unordered_list_text(text):
    block = text.split("\n")
    new_text = []
    for line in block:
        new_text.append(ParentNode("li", text_to_children(line[2:].strip())))
    return new_text

def get_code_block_text(text):
    return text[3:-3] 

def get_quote_text(text):
    block = text.split("\n")
    new_text = []
    for line in block:
        new_text.append(line.lstrip('>').strip())
    return " ".join(new_text)

str = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
#html = markdown_to_html_node(str)
#print(html.to_html())


md = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        

#md = "### this is a **heading**"
#node = markdown_to_html_node(md)
# print(node.to_html())
#"<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",

