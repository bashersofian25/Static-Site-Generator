from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
import re
from collections.abc import Iterable
from blocktype import BlockType


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

def markdown_to_blocks(markdown):
    blocks =  list(map(lambda block: block.strip(),markdown.split("\n\n")))
    filtered_blocks = list(filter(lambda block: block != "", blocks))
    return filtered_blocks

def is_block_heading(block):
    block_arr = block.split()
    for char in block_arr[0]:
        if(char != "#"):
            return False
    return True

def is_block_code(block):
    return block[:3] == "```" and block[-3:] == "```"

def all_block_lines_start_with(block, char):
    block_lines = block.split("\n")
    for line in block_lines:
        if line[0] != char:
            return False
        if line [1] != " " and line[0] != ">":
            return False
    return True

def is_block_qoute(block):
    return all_block_lines_start_with(block, ">")

def is_block_unordered_list(block):
    return all_block_lines_start_with(block, "-")

def is_block_ordered_list(block):
    return all_block_lines_start_with(block, ".")



def block_to_block_Type(block):
    if(is_block_heading(block)):
        return BlockType.HEADING
    elif(is_block_code(block)):
        return BlockType.CODE
    elif(is_block_qoute(block)):
        return BlockType.QUOTE
    elif(is_block_ordered_list(block)):
        return BlockType.ORDERED_LIST
    elif(is_block_unordered_list(block)):
        return BlockType.UNORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def heading_block_to_html_node(block):
    block_arr = block.split()
    heading_value = 0
    for char in block_arr[0]:
        if(char == "#"):
            heading_value += 1
        else:
            raise Exception ("Invalid heading Syntax!")
    return LeafNode(tag=f"{BlockType.HEADING.value}{heading_value}", value=" ".join(block_arr[1:]))


def code_block_to_html_node(block):
    return HTMLNode(tag="pre", children=[LeafNode(tag=BlockType.CODE.value, value=block[3:-3])])

def paragraph_block_to_html_node(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return HTMLNode(tag=BlockType.PARAGRAPH.value, children=html_nodes)

def qoute_block_to_html_node(block):
    block_arr = block.split(">")
    return LeafNode(tag=BlockType.QUOTE.value, value="".join(block_arr))



def list_block_to_html_node_children(block):
    block_arr = block.split("\n")
    list_html_nodes = []
    for line in block_arr:
        line_nodes = text_to_textnodes(line)
        child_html_nodes = []
        for text_node in line_nodes:
            child_html_nodes.append(text_node_to_html_node(text_node))
        list_html_nodes.append(HTMLNode(tag="li", children=child_html_nodes))
    return list_html_nodes
    

def ordered_list_block_to_html(block):
    return HTMLNode(tag=BlockType.ORDERED_LIST.value, children=list_block_to_html_node_children(block))


def unordered_list_block_to_html(block):
    return HTMLNode(tag=BlockType.UNORDERED_LIST.value, children=list_block_to_html_node_children(block))



def mdblock_to_htmlnode(block):
    block_type = block_to_block_Type(block)
    if(block_type == BlockType.HEADING):
        return heading_block_to_html_node(block)
    elif(block_type == BlockType.CODE):
        return code_block_to_html_node(block)
    elif(block_type == BlockType.PARAGRAPH):
        return paragraph_block_to_html_node(block)
    elif(block_type == BlockType.QUOTE):
        return qoute_block_to_html_node(block)
    elif(block_type == BlockType.ORDERED_LIST):
        return ordered_list_block_to_html(block)
    elif(block_type == BlockType.UNORDERED_LIST):
        return unordered_list_block_to_html(block)
    else:
        raise Exception("Invalid block type!")
        



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_nodes.append(mdblock_to_htmlnode(block))
    return HTMLNode(tag = "div", children=html_nodes)