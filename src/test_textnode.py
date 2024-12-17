import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_sum_is_none(self):
		node = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node.url, None)

	def test_sum_is_not_none(self):
		node = TextNode("This is a text node", TextType.BOLD, "https://test.com")
		self.assertEqual(node.url, "https://test.com")

	def test_italic(self):
		node = TextNode("This is a text node", TextType.ITALIC, "https://test.com")
		self.assertEqual(node.text_type, TextType.ITALIC)

	def test_html_node_normal(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = node.to_html_node()
		self.assertEqual(html_node.to_html(), "This is a text node")

	def test_html_node_bold(self):
		node = TextNode("This is a text node", TextType.BOLD)
		html_node = node.to_html_node()
		self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

	def test_html_node_link(self):
		node = TextNode("This is a link", TextType.LINKS, 'https://test.com').to_html_node()
		self.assertEqual(node.to_html(), '<a href="https://test.com">This is a link</a>')

	def test_html_node_image(self):
		node = TextNode("This is an image", TextType.IMAGES, 'https://test.com').to_html_node()
		self.assertEqual(node.to_html(), '<img src="https://test.com" alt="This is an image"></img>')

if __name__ == "__main__":
	unittest.main()
