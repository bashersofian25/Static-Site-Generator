import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def assert_url_is_none(self, node):
        self.assertEqual(node.url, None)
    
    def __assert_url_is_not_none(TextNode):
        return TextNode.url != None

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node3)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node3)

    def test_url_is_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assert_url_is_none(node)



if __name__ == "__main__":
    unittest.main()