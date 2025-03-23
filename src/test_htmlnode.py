import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "hi there", None, {"test":"myTest", "link":"myLink", "class":"myClass"})
        self.assertEqual(node.props_to_html(), ' test="myTest" link="myLink" class="myClass"')
    
    def test_repr(self):
        node = HTMLNode("p", "hi there", None, {"test":"myTest", "link":"myLink", "class":"myClass"})
        self.assertEqual(repr(node), f"tag: {node.tag}\nvalue: {node.value}\nchildren: {node.children}\nprops: {node.props}\n")

    def test_to_html_raises_error(self):
        node = HTMLNode("p", "hi there", None, {"test":"myTest", "link":"myLink", "class":"myClass"})
        self.assertRaises(NotImplementedError, node.to_html)

    def test_leaf_to_html_p(self):
        self.assertEqual(LeafNode("p", "This is a paragraph of text.").to_html(),\
        "<p>This is a paragraph of text.</p>")
    
    def test_leaf_to_html_a(self):
        self.assertEqual(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html(),\
        '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("span", "child")
        grandchild_node3 = LeafNode("span", "child")
        grandchild_node4 = LeafNode("span", "child")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2,\
         grandchild_node3, grandchild_node4])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><span>child</span><span>child</span><span>child</span></span></div>",
        )


if __name__ == "__main__":
    unittest.main()