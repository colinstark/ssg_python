import os
import shutil

from utils import extract_title, markdown_to_html_node

def main():
	purge_folder("public")
	copy_directory("static", "public")
	generate_page("content/index.md", "template.html", "public/index.html")

def purge_folder(target):
	shutil.rmtree(target, ignore_errors=True)
	os.mkdir(target)

def copy_directory(source, dest):
	if not os.path.exists(source):
		return

	shutil.rmtree(dest, ignore_errors=True)
	os.mkdir(dest)

	for item in os.listdir(source):
		src_item = os.path.join(source, item)
		dst_item = os.path.join(dest, item)

		if os.path.isfile(src_item):
			shutil.copy(src_item, dst_item)

		elif os.path.isdir(src_item):
			copy_directory(src_item, dst_item)

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

	with open(from_path, 'r') as mdf:
		md_file = mdf.read()

	with open(template_path, 'r') as f:
		template = f.read()

	html_content = markdown_to_html_node(md_file)
	html_title = extract_title(md_file)

	template = template.replace("{{ Title }}", html_title)
	template = template.replace("{{ Content }}", html_content)

	with open(dest_path, 'w') as file:
		file.write(template)

main()
