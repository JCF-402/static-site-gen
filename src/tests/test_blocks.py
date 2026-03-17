import unittest
from block import BlockType
from block import block_to_block

class TestBlocktoBlock(unittest.TestCase):
    def test_headings(self):
        block = "# This is a heading with 1"
        block_type = block_to_block(block)
        self.assertEqual(block_type,BlockType.HEADING)

        block2 = "### This is a heading with 3"
        block_type2 = block_to_block(block2)
        self.assertEqual(block_type2,BlockType.HEADING)
    
    def test_code(self):
        block = "``` This is a code block ```"
        block_type = block_to_block(block)
        self.assertEqual(block_type,BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote block"
        block_type = block_to_block(block)
        self.assertEqual(block_type,BlockType.QUOTE)
    
    def test_ordered_list(self):
        block = "1. This is number 1"
        block_type = block_to_block(block)
        self.assertEqual(block_type,BlockType.Or_List)

    def test_unordered_list(self):
        block = "- This is a weird list"
        block_type = block_to_block(block)
        self.assertEqual(block_type,BlockType.Un_List)

    def test_paragraph(self):
        block = "This is a paragraph"
        block_type = block_to_block(block)
        self.assertEqual(block_type,BlockType.PARAGRAPH)
if __name__ == "__main__":
    unittest.main()