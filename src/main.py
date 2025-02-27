from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_markdown import markdown_to_html_node
import os
import shutil

PUBLIC_FOLDER = "./public"
STATIC_FOLDER = "./static"
CONTENT_FOLDER = "./content"


def check_folder_path(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # print("Folder exists")

def delete_folder_content(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path,file_name)
        try:
            if os.path.isfile(file_path):
                print("DEL file:\t" + file_path)
                os.unlink(file_path)
            else:
                print("DEL folder:\t" + file_path)
                delete_folder_content(file_path)
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def copy_static_files(source_folder, destination_folder):
    for file_name in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, file_name)
        destination_file_path = os.path.join(destination_folder, file_name)
        try:
            if os.path.isfile(source_file_path):
                print("COPY file:\t" + source_file_path)
                shutil.copy(source_file_path, destination_file_path)
                
            else:
                print("COPY folder:\t" + source_file_path)
                check_folder_path(destination_file_path)
                copy_static_files(source_file_path, destination_file_path)
        except Exception as e:
            print(f"Failed to copy {source_file_path}. Reason: {e}")

def extract_title(markdown_file):
    with open(markdown_file, "r") as file:
        markdown = file.readline()
        if markdown.startswith("# "):
            return markdown[2:].strip()
        raise Exception("Title not found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as md_file:
        md_content = md_file.read()
        with open(template_path, "r") as file:
            template = file.read()
            html_content = markdown_to_html_node(md_content).to_html()
            title = extract_title(from_path)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html_content)
            dest_path = dest_path.replace(".md", ".html")
            with open(dest_path, "w") as file:
                file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file_name in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, file_name)
        dest_path = os.path.join(dest_dir_path, file_name)
        if os.path.isdir(file_path):
            check_folder_path(dest_path)
            generate_pages_recursive(file_path, template_path, dest_path)
        elif file_name.endswith(".md"):
            generate_page(file_path, template_path, dest_path)

def main():
    check_folder_path(PUBLIC_FOLDER)
    delete_folder_content(PUBLIC_FOLDER)
    copy_static_files(STATIC_FOLDER, PUBLIC_FOLDER)
#    generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(CONTENT_FOLDER, "template.html", PUBLIC_FOLDER)














#     text_node = TextNode("Hello world", TextType.BOLD, "https://www.google.com")
#     print(text_node)

#     html_node = HTMLNode("div", "Hello world", ["a"], {"href": "https://www.google.com"})
#     print(html_node)

#     node = ParentNode(
#     "p",
#     [
#         LeafNode("b", "Bold text"),
#         LeafNode(None, "Normal text"),
#         LeafNode("i", "italic text"),
#         LeafNode(None, "Normal text"),
#     ],
# )

#     print(node.to_html())



main()