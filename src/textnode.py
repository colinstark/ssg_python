from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINKS = "links"
	IMAGES = "images"

class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"

	def to_html_node(self):
		match self.text_type:
			case TextType.TEXT:
				return LeafNode(None, self.text)

			case TextType.BOLD:
				return LeafNode("b", self.text)

			case TextType.ITALIC:
				return LeafNode("i", self.text)

			case TextType.ITALIC:
				return LeafNode("i", self.text)

			case TextType.CODE:
				return LeafNode("code", self.text)

			case TextType.LINKS:
				return LeafNode("a", self.text, {"href": self.url})

			case TextType.IMAGES:
				return LeafNode("img", "", {"src": self.url, "alt": self.text})

		raise Exception("Wrong type")
