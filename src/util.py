from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.LINK:
        return LeafNode(text_node.text_type.value, text_node.text, {"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(text_node.text_type.value, None, {"src":text_node.url, "alt":text_node.text})
    else:
        return LeafNode(text_node.text_type.value, text_node.text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if delimiter not in old_node.text:
            raise Exception(f"invalid mardown, delimiter '{delimiter}' not found in text.")
        old_node_split = old_node.text.split(delimiter)
        if len(old_node_split) % 2 == 0:
            raise Exception(f"invalid markdown, no closing delimiter '{delimiter}' found.")
        for index, section in enumerate(old_node_split):
            if index % 2 != 0:
                new_nodes.append(TextNode(section, text_type))
            else:
                new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes
