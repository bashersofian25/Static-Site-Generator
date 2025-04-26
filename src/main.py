from textnode import TextType
from textnode import TextNode
from public_prep import prepare_directory, generate_page, generate_pages_recursive

def main():
    prepare_directory()
    generate_pages_recursive("content", "template.html","public")



main()