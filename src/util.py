from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.LINK:
        return LeafNode(text_node.text_type.value, text_node.text, {"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(text_node.text_type.value, None, {"src":text_node.url, "alt":text_node.text})
    else:
        return LeafNode(text_node.text_type.value, text_node.text)

