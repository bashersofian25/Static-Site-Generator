from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
import re
from collections.abc import Iterable


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
            new_nodes.append(old_node)
            continue
        old_node_split = old_node.text.split(delimiter)
        if len(old_node_split) % 2 == 0:
            raise Exception(f"invalid markdown, no closing delimiter '{delimiter}' found.")
        for index, section in enumerate(old_node_split):
            if index % 2 != 0:
                new_nodes.append(TextNode(section, text_type))
            else:
                new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    listOfImageTuples = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return listOfImageTuples

def extract_markdown_links(text):
    listOfLinkTuples = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return listOfLinkTuples

def flatten(xss):
    return [
        x 
        for elem in xss 
        for x in (elem if isinstance(elem, Iterable) and not isinstance(elem, (str, bytes)) else [elem])
    ]

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        temp_nodes = [node]
        for image in images:
            delimeter = f"![{image[0]}]({image[1]})"
            for indexForTemp, temp_node in enumerate(temp_nodes):
                split_collection = []
                if temp_node.text_type == TextType.TEXT:
                    split=temp_node.text.split(delimeter)
                    for index, text in enumerate(split):
                        if index %2 == 0:
                            split_collection.append(TextNode(text, TextType.TEXT))
                        else:
                            split_collection.append(TextNode(image[0], TextType.IMAGE, image[1]))
                            if text != None  and text != "":
                                split_collection.append(TextNode(text, TextType.TEXT))
                else:
                    split_collection.append(temp_nodes[indexForTemp])
                temp_nodes[indexForTemp] = split_collection
                temp_nodes = flatten(temp_nodes)
                
        new_nodes.extend(temp_nodes)
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        temp_nodes = [node]
        for link in links:
            delimeter = f"[{link[0]}]({link[1]})"
            for indexForTemp, temp_node in enumerate(temp_nodes):
                split_collection = []
                if temp_node.text_type == TextType.TEXT:
                    split=temp_node.text.split(delimeter)
                    for index, text in enumerate(split):
                        if index %2 == 0:
                            split_collection.append(TextNode(text, TextType.TEXT))
                        else:
                            split_collection.append(TextNode(link[0], TextType.LINK, link[1]))
                            if text != None and text != "":
                                split_collection.append(TextNode(text, TextType.TEXT))
                else:
                    split_collection.append(temp_nodes[indexForTemp])
                temp_nodes[indexForTemp] = split_collection
                temp_nodes = flatten(temp_nodes)  
        new_nodes.extend(temp_nodes)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    if "**" in text:
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    if "_" in text:
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    if "`" in text:
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)

    return nodes