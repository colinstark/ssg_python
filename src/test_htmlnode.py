import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
	#def test_eq_basic(self):
	#	node = HTMLNode("div", None, None, None)
	#	node2 = HTMLNode("div", None, None, None)
	#	self.assertEqual(node, node2)

	def test_value(self):
		node = HTMLNode("div", "hello")
		self.assertEqual(node.value, "hello")

	def test_children(self):
		node = HTMLNode("div", "", ["one", "two"])
		self.assertEqual(node.children, ["one", "two"])

	def test_props(self):
		node = HTMLNode("a", None, None, {"href": "https://test.com"})
		self.assertEqual(node.props, {"href": "https://test.com"})

	def test_leaf_basic(self):
		node = LeafNode("p", "This is a paragraph of text.")
		self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

	def test_leaf_params(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

	def test_parent_basic(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
			],
		)
		self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')


	def test_parent_parent(self):
		node = ParentNode(
			"div",
			[
				ParentNode(
					"p",
					[
						LeafNode("i", "italic text"),
						LeafNode(None, "Normal text"),
					]
				),
				LeafNode("b", "Bold text"),
			],
		)
		self.assertEqual(node.to_html(), '<div><p><i>italic text</i>Normal text</p><b>Bold text</b></div>')



if __name__ == "__main__":
	unittest.main()
