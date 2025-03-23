from textnode import TextType
from textnode import TextNode

def main():
    first_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print (repr(first_text_node))

main()