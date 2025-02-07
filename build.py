import click
import os
import yaml
import markdown
from typing import Optional, Tuple, Any, List
from jinja2 import Environment, FileSystemLoader
from models import Post, Page
from util import FilePath, write_error_msg, write_warning_msg

@click.command()
def build():
    if is_moku_project_dir():
        build_output_from_user_project()
    else:
        write_error_msg("not in a valid project directory")

def is_moku_project_dir() -> bool:
    return os.path.isfile(os.path.join(os.getcwd(), ".moku"))
    
def build_output_from_user_project():
    env = Environment(loader=FileSystemLoader(FilePath.TEMPLATE_DIR.project_path))
    posts: List[Post] = get_posts()
    pages: List[Page] = get_pages()

    os.makedirs(FilePath.OUTPUT_DIR.cwd_path)
    os.makedirs(FilePath.OUTPUT_POSTS.cwd_path)

    build_pages(env=env, pages=pages, posts=posts)
    build_post_pages(env=env, posts=posts)

# TODO: implement multiple root pages
def build_pages(env: Environment, pages: List[Page], posts: List[Post]):
    index_template = env.get_template("index.html")

    for page in pages:
        rendered_index = index_template.render(
                title=page.title,
                description=page.description,
                posts=posts
        )
        with open(os.path.join(FilePath.OUTPUT_DIR.cwd_path, "index.html"), "w", encoding="utf-8") as f:
            f.write(rendered_index)
        
def build_post_pages(env: Environment, posts: List[Post]):
    post_template = env.get_template("post.html")

    for post in posts:
        rendered_html = post_template.render(title=post.title, content=post.html_content)
        output_dir = os.path.join(FilePath.OUTPUT_POSTS.cwd_path, post.slug)
        os.makedirs(output_dir)

        output_path = os.path.join(output_dir, "index.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

def get_posts() -> List[Post]:
    posts: List[Post] = []
    content_dir = FilePath.POSTS_DIR.cwd_path

    for filename in os.listdir(content_dir):
        if filename.endswith(".md"):
            slug = os.path.splitext(filename)[0]
            result = parse_markdown(content_dir, filename)
            if result:
                metadata, html_content = result
                post = Post(
                        title=metadata.get("title", "Untitled"),
                        date=metadata.get("date", "Unknown Date"),
                        html_content=html_content,
                        slug=slug
                        )
                posts.append(post)
            else:
                continue

    posts.sort(key=lambda x: x.date, reverse=True)

    return posts

def get_pages() -> List[Page]:
    pages: List[Page] = []
    content_dir = FilePath.CONTENT_DIR.cwd_path

    for filename in os.listdir(content_dir):
        if filename.endswith(".md"):
            slug = os.path.splitext(filename)[0]
            result = parse_markdown(content_dir, filename)
            if result:
                metadata, html_content = result
                page = Page(
                        title=metadata.get("title", "Untitled"),
                        date=metadata.get("date", "Unknown Date"),
                        description = html_content,
                        slug=slug
                        )
                pages.append(page)
            else:
                continue
    return pages

def parse_markdown(path: str, file_name: str) -> Optional[Tuple[Any, str]]:
    full_path = os.path.join(path, file_name)

    try: 
        with open(full_path, "r", encoding="utf-8") as md_file:
            file_content = md_file.read()
    except FileNotFoundError:
        write_error_msg(f"failed to open file {file_name}")
        return None
    except:
        write_error_msg(f"unknown while opening {file_name}")
        return None

    if file_content.startswith("---"):
        parts = file_content.split("---", 2)
        metadata = yaml.safe_load(parts[1])
        md_content = str(parts[2].strip())
    else:
        write_warning_msg("metadata missing in {file_name}")
        return

    html_content = markdown.markdown(md_content)

    return metadata, html_content
