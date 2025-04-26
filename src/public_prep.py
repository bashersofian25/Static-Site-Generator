import os
from util import markdown_to_html_node


def empty_public_directory_directory():
    os.system('rm -rf ./public/*')

def cp_static_to_public():
    os.system('cp -r ./static/* ./public/')



def prepare_directory():
    empty_public_directory_directory()
    cp_static_to_public()


def extract_title(markdown):
    markdown_lines = markdown.split("\n")
    for line in markdown_lines:
        if line[:2] == "# ":
            return line[2:].strip()  
    raise Exception("No header found")

def read_file_as_string(path):
    lines = []
    with open(path) as file:
        lines.append(file.read())
    file.close()
    return "\n".join(lines)

def write_content_to_file(path, content):
    content_lines = content.split("\n")
    counter = 0
    file = open(path, "w")
    file.write(f"{content_lines[0]}")
    file.close()
    file = open(path, "a")
    for line in content_lines:
        if counter == 0:
            counter += 1
            continue
        file.write("\n")
        file.write(f"{line}")
    file.close()
        

    



def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_content = read_file_as_string(from_path)
    template_content = read_file_as_string(template_path)
    title = extract_title(md_content)
    page_content = template_content.replace("{{ Title }}", title)
    page_content = page_content.replace("{{ Content }}", markdown_to_html_node(md_content).to_html())
    write_content_to_file(dest_path, page_content)

def clone_directory_structure(source_dir, target_dir):
    dir_content = os.listdir(source_dir)
    for item in dir_content:
        if os.path.isfile(f"{source_dir}/{item}"):
            continue
        else:
            os.mkdir(f"{target_dir}/{item}")
            clone_directory_structure(f"{source_dir}/{item}", f"{target_dir}/{item}")




def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_content = os.listdir(dir_path_content)
    for item in dir_content:
        
        if os.path.isfile(f"{dir_path_content}/{item}"):
            if item[-3:] == ".md":
                generate_page(f"{dir_path_content}/{item}", template_path, f"{dest_dir_path}/{item}".replace("content/", "public/").replace(".md", ".html"))
        else:
            generate_pages_recursive(f"{dir_path_content}/{item}", template_path, f"{dest_dir_path}/{item}".replace("content/", "public/"))
            
                


