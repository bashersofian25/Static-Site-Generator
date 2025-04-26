from textnode import TextType
from textnode import TextNode
from public_prep import prepare_directory, generate_page, generate_pages_recursive, clone_directory_structure
from sys import argv

def main(): 
    try:
        basepath = argv[1]
    except:
        basepath = "/"
    prepare_directory("docs")
    clone_directory_structure("content", "docs")
    generate_pages_recursive("content", "template.html","docs", basepath)



main()