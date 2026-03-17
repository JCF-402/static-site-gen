import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("p","text",None,props)
        expected =  ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected,node.props_to_html())

    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("p","text",None,props)
        expected = f'HTMLNode(p, text, None, {props})'
        print(node)

    def test_data_members(self):
        node = HTMLNode("p","text",None,None)
        self.assertEqual(node.tag,"p")
        self.assertEqual(node.value,"text")
        self.assertEqual(node.children,None)
        self.assertEqual(node.props,None)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p","Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a","Click me!",{"href":"https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>')
    def test_leaf_to_html_raises_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_leaf_to_html_tag_returns_text(self):
        node = LeafNode(None,"text")
        self.assertEqual(node.to_html(),"text")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_value_error_child(self):
        parent_node = ParentNode("b",None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_value_error_tag(self):
        child_node = LeafNode("span","child")
        parent_node = ParentNode(None,[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()