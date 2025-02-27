from textnode import TextNode, TextType

import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
    
        tmp_node = node.text.split(delimiter)
        if len(tmp_node) % 2 == 0:
            raise ValueError("Invalid Markdown syntax")
        for i in range(len(tmp_node)):
            if tmp_node[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(tmp_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(tmp_node[i], text_type))
            
            #new_nodes.append(TextNode(n, text_type))

    return new_nodes

# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     for old_node in old_nodes:
#         if old_node.text_type != TextType.TEXT:
#             new_nodes.append(old_node)
#             continue
#         split_nodes = []
#         sections = old_node.text.split(delimiter)
#         if len(sections) % 2 == 0:
#             raise ValueError("invalid markdown, formatted section not closed")
#         for i in range(len(sections)):
#             if sections[i] == "":
#                 continue
#             if i % 2 == 0:
#                 split_nodes.append(TextNode(sections[i], TextType.TEXT))
#             else:
#                 split_nodes.append(TextNode(sections[i], text_type))
#         new_nodes.extend(split_nodes)
#     return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    #matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

'''
from boot.dev
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
'''

#print(extract_markdown_links("This is a linasdf"))

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        old_text = node.text
        for match in matches:
            words = old_text.split(f"[{match[0]}]({match[1]})", 1)
            if words[0] != "":
                new_nodes.append(TextNode(words[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            old_text = words[1]
        if old_text != "":
            new_nodes.append(TextNode(old_text, TextType.TEXT))
    return new_nodes
            

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
       if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

       matches = extract_markdown_images(node.text)
       if len(matches) == 0:
            new_nodes.append(node)
            continue

       old_text = node.text
       for match in matches:
            words = old_text.split(f"![{match[0]}]({match[1]})", 1)
            if words[0] != "":
                new_nodes.append(TextNode(words[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            old_text = words[1]
        
       if old_text != "":
           new_nodes.append(TextNode(old_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes) 
    return nodes




text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
#print(text_to_textnodes(text))



