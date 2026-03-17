import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node",TextType.BOLD)
        self.assertNotEqual(node,node2)

    def test_url_eq(self):
        node = TextNode("Text",TextType.BOLD,None)
        node2 = TextNode("Text",TextType.BOLD,None)
        self.assertEqual(node,node2)

    def test_url_not_eq(self):
        node = TextNode("Text",TextType.BOLD,None)
        node2 = TextNode("Text",TextType.BOLD,"link")
        self.assertNotEqual(node,node2)

    def test_type_not_eq(self):
        node = TextNode("Text",TextType.BOLD)
        node2 = TextNode("Text",TextType.ITALIC)
        self.assertNotEqual(node,node2)

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_type_exception(self):
        node = TextNode("This is a text node", "whatever")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


class TestNodesDelimiter(unittest.TestCase):
    # Test Cases for each delimiter type
    # Test Cases for multiple nodes in list
    # Test cases for multiple delimiter types (future)

    def test_code_block(self):
        node = TextNode("This is text with a `code block` word",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"`",TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word",TextType.TEXT)
            ]

        )
    def test_empty_string_at_end(self):
        node = TextNode("This is text with a `code block`",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"`",TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ]
        )

    def test_unmatched_delimiter(self):
        node = TextNode("This is text with a `code block",TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node],"`",TextType.CODE)

    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**",TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.CODE),
                TextNode(" word",TextType.TEXT)
            ]

        )
if __name__ == "__main__":
    unittest.main()