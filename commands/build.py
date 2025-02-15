import click
import os
import re
import yaml
import shutil
import markdown
from typing import Optional, Tuple, Any, List
from jinja2 import Environment, FileSystemLoader
from utilities.models import Post, Page, TemplateType
from utilities.util import FilePath, write_error_msg, write_warning_msg, is_moku_project_dir

@click.command()
def build():
    if is_moku_project_dir():
        build_output_from_user_project()
    else:
        write_error_msg("not in a valid project directory")

def build_output_from_user_project():
    if os.path.exists(FilePath.OUTPUT_DIR.cwd_path):
        shutil.rmtree(FilePath.OUTPUT_DIR.cwd_path)

    env = Environment(loader=FileSystemLoader(FilePath.TEMPLATE_DIR.project_path))
    posts: List[Post] = get_posts()
    pages: List[Page] = get_pages()

    os.makedirs(FilePath.OUTPUT_DIR.cwd_path)
    os.makedirs(FilePath.OUTPUT_POSTS.cwd_path)

    build_pages(env=env, pages=pages, posts=posts)
    build_post_pages(env=env, posts=posts)
    copy_styles()
    copy_assets()

def build_pages(env: Environment, pages: List[Page], posts: List[Post]):
    for page in pages:
        page_template = env.get_template(page.template.value)
        if page.slug == "index":
            path = FilePath.OUTPUT_DIR.cwd_path
            rendered_index = page_template.render(
                title=page.title,
                description=page.description,
                posts=posts
            )
        else:
            path = os.path.join(FilePath.OUTPUT_DIR.cwd_path, page.slug)
            os.makedirs(path)
            rendered_index = page_template.render(
                title=page.title,
                description=page.description,
            )
        
        with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
            f.write(rendered_index)
        
def build_post_pages(env: Environment, posts: List[Post]):
    post_template = env.get_template("post.html")

    for post in posts:
        rendered_html = post_template.render(title=post.title, content=post.html_content, date=post.date)
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
            result = parse_markdown(content_dir, filename, "post")
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
            result = parse_markdown(content_dir, filename, "page")
            if result:
                metadata, html_content = result
                page = Page(
                        title=metadata.get("title", "Untitled"),
                        date=metadata.get("date", "Unknown Date"),
                        template=TemplateType.from_string(metadata.get("template", "page.html")),
                        description = html_content,
                        slug=slug
                        )
                pages.append(page)
            else:
                continue
    return pages

def parse_markdown(path: str, file_name: str, content_type: str ) -> Optional[Tuple[Any, str]]:
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

    md_content = re.sub(
            r'!\[(.*?)\]\((.*?)\)', 
            lambda match: normalize_image_path(match, content_type), 
            md_content
            )

    html_content = markdown.markdown(
            md_content,
            extensions=[
                'fenced_code',
                'codehilite',
                'tables'
                ]
            )

    return metadata, html_content

def copy_styles():
    source = os.path.join(FilePath.STATIC_DIR.cwd_path, "styles.css")
    destination = os.path.join(FilePath.OUTPUT_DIR.cwd_path, "styles.css")

    try: 
        shutil.copy(source,destination)
    except FileNotFoundError:
        write_error_msg("styles.css not found in static directory")
    except Exception:
        write_error_msg("unknown while trying to copy styles.css ")

def copy_assets():
    source = os.path.join(FilePath.ASSETS_DIR.cwd_path)
    destination = os.path.join(FilePath.OUTPUT_DIR.cwd_path, "assets")
    
    try: 
        shutil.copytree(source, destination)
    except FileNotFoundError:
        write_warning_msg("assets directory missing")
    except Exception as e:
        write_error_msg(f"unknown while trying to copy assets {e}")

def normalize_image_path(match, content_type: str):
    alt_text = match.group(1)
    filename = os.path.basename(match.group(2))

    if content_type == "post":
        new_path = os.path.join("./../../assets", filename)
    else:
        new_path = os.path.join("assets", filename)

    return f"![{alt_text}]({new_path})"
