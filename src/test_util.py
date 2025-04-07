import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

from util import text_node_to_html_node, split_nodes_delimiter,\
     extract_markdown_images, extract_markdown_links,\
     split_nodes_links, split_nodes_images


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src":"www.image.com", "alt":"This is an image node"})

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"www.link.com"})
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    def test_non_ext_type_node(self):
        node = TextNode("print('hi')", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("print('hi')", TextType.CODE),
        ])
    def test_no_closing_delim(self):
        node = TextNode("This is text with a `code block", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, ([node], "`", TextType.CODE))

    def test_no_delim(self):
        node = TextNode("This is text with a code block", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, ([node], "`", TextType.CODE))
    
    def test_multi_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with another `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with another ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

class TestMarkdownImageExtracter(unittest.TestCase):
    def test_no_spaces(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        self.assertEqual(extract_markdown_images(text), [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ])


class TestMarkdownLinkExtracter(unittest.TestCase):
    def test_no_spaces(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        self.assertEqual(extract_markdown_links(text), [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ])


class TestLinkAndImageSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_multinode_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a [third link from second node](https://i.imgur.com/zjjcJKZ.png) and [fourth link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("third link from second node", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "fourth link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_multinode_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a ![third image from second node](https://i.imgur.com/zjjcJKZ.png) and ![fourth image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("third image from second node", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "fourth image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_images_with_no_images(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode(
                "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
                )
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()