import os
import sys
import shutil

from utils import extract_title, markdown_to_html_node

def main():
	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	else:
		basepath = "/"

	purge_folder("docs")
	copy_directory("static", "docs")
	generate_pages_recursive(basepath, "content", "template.html", "docs")

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

def generate_page(basepath, from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

	with open(from_path, 'r') as mdf:
		md_file = mdf.read()

	with open(template_path, 'r') as f:
		template = f.read()

	html_content = markdown_to_html_node(md_file)
	html_title = extract_title(md_file)

	template = template.replace("{{ Title }}", html_title)
	template = template.replace("{{ Content }}", html_content)

	template = template.replace('href="/', f'href="{basepath}')
	template = template.replace('src="/', f'src="{basepath}')

	with open(dest_path, 'w') as file:
		file.write(template)


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
	print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}.")

	for entry in os.scandir(dir_path_content):
		print("ENTRY", entry)
		if entry.is_file() and entry.name.endswith('.md'):
			print("IS FILE", entry, entry.name)
			generate_page(basepath, os.path.join(dir_path_content, entry.name), template_path, os.path.join(dest_dir_path, entry.name.replace(".md", ".html")))

		elif entry.is_dir():
			print("IS DIR", dest_dir_path)
			os.makedirs(os.path.join(dest_dir_path, entry.name), exist_ok=True)
			generate_pages_recursive(basepath, os.path.join(dir_path_content, entry.name), template_path, os.path.join(dest_dir_path, entry.name))


main()
