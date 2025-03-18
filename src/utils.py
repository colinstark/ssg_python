import re
from textnode import TextNode, TextType

link_regex = r"\[(.+?)\]\((.+?)\)"
image_regex = r"!\[(.+?)\]\((.+?)\)"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        parts = []

        # Keep processing the text until no more delimiters are found
        while delimiter in text:
            # Find the first delimiter
            start_idx = text.find(delimiter)
            if start_idx > 0:
                # Add text before delimiter as TEXT
                parts.append((text[:start_idx], TextType.TEXT))

            # Find the second delimiter
            remaining = text[start_idx + len(delimiter):]
            end_idx = remaining.find(delimiter)

            if end_idx == -1:
                # No closing delimiter found
                parts.append((text[start_idx:], TextType.TEXT))
                text = ""
                break

            # Add the delimited text with the special type
            delimited_text = remaining[:end_idx]
            parts.append((delimited_text, text_type))

            # Continue with the rest of the text
            text = remaining[end_idx + len(delimiter):]

        # Add any remaining text
        if text:
            parts.append((text, TextType.TEXT))

        # Create TextNodes from the parts
        for part_text, part_type in parts:
            new_nodes.append(TextNode(part_text, part_type))

    return new_nodes


def split_nodes_link(old_nodes):
	nodes = []
	if len(old_nodes) == 0: return nodes

	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			nodes.append(node)
		else:
			chunks = re.split(r"(.+?)(?P<link>\[.+?\]\(.+?\))", node.text)
			chunks = list(filter(lambda x: x != "", chunks))
			for i in range(0, len(chunks)):
				current = chunks[i]
				url_parts = re.findall(link_regex, current)
				if len(url_parts) > 0:
					nodes.append(TextNode(url_parts[0][0], TextType.LINKS, url_parts[0][1]))
				else:
					nodes.append(TextNode(current, TextType.TEXT))

	return nodes

def split_nodes_image(old_nodes):
	nodes = []
	if len(old_nodes) == 0: return nodes

	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			nodes.append(node)
		else:
			chunks = re.split(r"(.+?)(?P<link>!\[.+?\]\(.+?\))", node.text)
			chunks = list(filter(lambda x: x != "", chunks))
			for i in range(0, len(chunks)):
				current = chunks[i]
				url_parts = re.findall(image_regex, current)
				if len(url_parts) > 0:
					nodes.append(TextNode(url_parts[0][0], TextType.IMAGES, url_parts[0][1]))
				else:
					nodes.append(TextNode(current, TextType.TEXT))

	return nodes

def extract_markdown_images(text):
	images = re.findall(image_regex, text)
	return images

def extract_markdown_links(text):
	links = re.findall(link_regex, text)
	return links

def text_to_textnodes(text):
	nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	if extract_markdown_images(text):
		nodes = split_nodes_image(nodes)

	if extract_markdown_links(text):
		nodes = split_nodes_link(nodes)

	return nodes

def markdown_to_blocks(markdown):
	block_strings = markdown.split("\n\n")
	block_strings = list(map(lambda x: x.strip("\n\t"), block_strings))
	block_strings = list(filter(lambda x: x != "", block_strings))

	return block_strings

def block_to_block_type(block):
	if re.match(r"\#{1,6}\s", block):
		return "heading"

	if re.match(r"^```.+```", block):
		return "code"

	lines = block.split("\n")

	if lines[0] == "```" and lines[-1] == "```":
		return "code"


	results = list(map(lambda x: x.startswith("> "), lines))
	if all(results):
		return "quote"

	results = list(map(lambda x: re.search(r"^\*\s|-\s", x), lines))
	if all(results):
		return "unordered_list"

	results = list(map(lambda x: re.match(r"^(\d+?)\.\s", x), lines))
	index = 0
	for i in range(0, len(results)):
		if results[i] != None:
			res = int(results[i].groups()[0])
			if res > index:
				index = res
			else:
				results.append(None)

	if all(results):
		return "ordered_list"

	return "paragraph"

def headline_level(block):
	print("HL", block)
	if block.startswith("# "):
		return "h1", block.lstrip("# ")
	if block.startswith("## "):
		return "h2", block.lstrip("## ")
	if block.startswith("### "):
		return "h3", block.lstrip("### ")
	if block.startswith("#### "):
		return "h4", block.lstrip("#### ")
	if block.startswith("##### "):
		return "h5", block.lstrip("##### ")
	if block.startswith("###### "):
		return "h6", block.lstrip("###### ")

def convert_text(text):
	nodes = text_to_textnodes(text)
	nodes = list(map(lambda x: x.to_html_node(), nodes))
	nodes = list(map(lambda x: x.to_html(), nodes))

	return "".join(nodes)

def markdown_to_html_node(markdown):
	results = []
	blocks = markdown_to_blocks(markdown)

	for block in blocks:
		match block_to_block_type(block):
			case "unordered_list":
				lis = block.split("\n")
				lis = list(map(lambda x: f"<li>{convert_text(x[2:])}</li>", lis))
				results.append(f"<ul>{''.join(lis)}</ul>")

			case "ordered_list":
				lis = block.split("\n")
				lis = list(map(lambda x: f"<li>{convert_text(x.partition(". ")[2])}</li>", lis))
				results.append(f"<ol>{''.join(lis)}</ol>")

			case "code":
				block = block.strip("```\n").strip("```")
				results.append(f"<pre><code>{block}</code></pre>")

			case "heading":
				hl, content = headline_level(block)
				results.append(f"<{hl}>{convert_text(content)}</{hl}>")

			case "quote":
				block = block.strip("> ")
				results.append(f"<blockquote>{block}</blockquote>")

			case "paragraph":
				results.append(f"<p>{convert_text(block)}</p>")


	return f"<div>{''.join(results)}</div>"

def extract_title(markdown):
	blocks = markdown_to_blocks(markdown)
	blocks = list(filter(lambda x: x.startswith("# "), blocks))
	if len(blocks) == 0:
		raise Exception("No headline")
	else:
		return blocks[0].lstrip("# ")
