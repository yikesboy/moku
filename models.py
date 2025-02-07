from dataclasses import dataclass
from enum import Enum

class TemplateType(Enum):
    POST = "post.html"
    INDEX = "index.html"

@dataclass
class Post():
    title: str
    date: str
    html_content: str
    slug: str
    template: TemplateType = TemplateType.POST

@dataclass
class Page():
    title: str
    date: str
    description: str
    slug: str
    template: TemplateType = TemplateType.INDEX
