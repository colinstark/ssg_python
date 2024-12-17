class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def __repr__(self):
		return f"HTML node(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		props = []

		if self.props == None:
			return ""

		for prop in self.props:
			props.append(f"{prop}=\"{self.props[prop]}\" ")

		return "".join(props).rstrip()

	def space_if_props(self):
		if self.props and len(self.props) > 0:
			return " "
		else:
			return ""

class LeafNode(HTMLNode):
	def __init__(self, tag=None, value=None, props=None):
		super()
		self.tag = tag
		self.value = value
		self.props = props

	def __repr__(self):
		return f"Leaf node(tag: {self.tag}, value: {self.value}, props: {self.props})"

	def to_html(self):
		if self.value == None:
			raise ValueError

		if self.tag == None:
			return self.value

		return f"<{self.tag}{self.space_if_props()}{self.props_to_html().rstrip()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super()
		self.tag = tag
		self.children = children
		self.props = props

	def __repr__(self):
		return f"Parent node(tag: {self.tag}, children: {self.children}, props: {self.props})"

	def to_html(self):
		if self.tag == None:
			raise ValueError("No Tag!")

		if self.children == None:
			raise ValueError("No children!")

		children = ""
		for child in self.children:
			children += child.to_html()

		return f"<{self.tag}>{children}</{self.tag}>"
