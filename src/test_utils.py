import unittest

from utils import block_to_block_type, extract_markdown_links, extract_title, markdown_to_blocks, markdown_to_html_node, split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
	def test_splitting(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(new_nodes[1].text_type, TextType.CODE)

	def test_splitting_two(self):
		node = TextNode("This is `code` with a `code block`", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(new_nodes[3].text_type, TextType.CODE)
		self.assertEqual(new_nodes[3].text, "code block")

	def test_splitting_italic(self):
		node = TextNode("This is text with a *italic* word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
		self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

	def test_splitting_bold(self):
		node = TextNode("This is text with a **bold** word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

	def test_splitting_links(self):
		node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
		new_nodes = split_nodes_link([node])
		self.assertEqual(new_nodes[1].text_type, TextType.LINKS)

	def test_splitting_images(self):
		node = TextNode("This is text with an image ![boot dev](https://www.boot.dev/logo.png) and ![youtube](https://www.youtube.com/logo.jpg)", TextType.TEXT)
		new_nodes = split_nodes_image([node])
		self.assertEqual(new_nodes[1].text_type, TextType.IMAGES)

	def test_image_regex(self):
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		images = extract_markdown_images(text)
		self.assertEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

	def test_link_regex(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		links = extract_markdown_links(text)
		self.assertEqual(links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

	def test_all_node_conversions(self):
		text = "This is **text** with an *italic* word and a `code block` and **an** ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		nodes = text_to_textnodes(text)
		self.assertEqual(nodes, [
				TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word and a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" and ", TextType.TEXT),
				TextNode("an", TextType.BOLD),
				TextNode(" ", TextType.TEXT),
				TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode(" and a ", TextType.TEXT),
				TextNode("link", TextType.LINKS, "https://boot.dev"),
			]
		)

	def test_block_conversion(self):
		md = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
		"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(blocks, [
			'# This is a heading',
			'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
			'* This is the first list item in a list block\n* This is a list item\n* This is another list item'
		])

	def test_block_type_heading(self):
		block_type = block_to_block_type("## Test")
		self.assertEqual(block_type, "heading")

	def test_block_type_code(self):
		block_type = block_to_block_type("```testFunction()```")
		self.assertEqual(block_type, "code")

	def test_block_type_quote(self):
		block_type = block_to_block_type("> A quote \n> You know")
		self.assertEqual(block_type, "quote")

	def test_block_type_ul(self):
		block_type = block_to_block_type("* A list \n* You know")
		self.assertEqual(block_type, "unordered_list")

	def test_block_type_ul_fail(self):
		block_type = block_to_block_type("- A list \n· You know")
		self.assertEqual(block_type, "paragraph")

	def test_block_type_ol(self):
		block_type = block_to_block_type("1. A list \n2. You know")
		self.assertEqual(block_type, "ordered_list")

	def test_block_type_ol_fail(self):
		block_type = block_to_block_type("2. A list \n You know")
		self.assertEqual(block_type, "paragraph")

	def test_block_type_ol_fail_order(self):
		block_type = block_to_block_type("2. A list \n1. You know")
		self.assertEqual(block_type, "paragraph")

	def test_md_to_html_hp(self):
		res = markdown_to_html_node("# Hi there\n\n## Subheadline\n\nThis is **the** hook")
		self.assertEqual(res, "<div><h1>Hi there</h1><h2>Subheadline</h2><p>This is <b>the</b> hook</p></div>")

	def test_md_to_html_ul(self):
		res = markdown_to_html_node("#### Unordered\n\n* One\n* Two")
		self.assertEqual(res, "<div><h4>Unordered</h4><ul><li>One</li><li>Two</li></ul></div>")

	def test_md_to_html_ol(self):
		res = markdown_to_html_node("### Ordered\n\n1. One\n2. Two")
		self.assertEqual(res, "<div><h3>Ordered</h3><ol><li>One</li><li>Two</li></ol></div>")

	def test_extract_title(self):
		title = extract_title("# Hi there\n\n Oh hey Mark")
		self.assertEqual(title, "Hi there")

if __name__ == "__main__":
	unittest.main()
