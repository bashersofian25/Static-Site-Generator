from textnode import TextType
from textnode import TextNode
from public_prep import prepare_directory, generate_page, generate_pages_recursive, clone_directory_structure

def main():
    prepare_directory()
    clone_directory_structure("content", "public")
    generate_pages_recursive("content", "template.html","public")



main()