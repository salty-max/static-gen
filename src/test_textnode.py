import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("Pikachu", "bold")
        node2 = TextNode("Eevee", "bold")
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("Pikachu", "bold")
        node2 = TextNode("Pikachu", "italic")
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("Pikachu", "bold")
        node2 = TextNode("Pikachu", "bold", "https://pallettown.kanto")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
