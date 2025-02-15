from dataclasses import dataclass
from enum import Enum

class TemplateType(Enum):
    POST = "post.html"
    INDEX = "index.html"
    PAGE = "page.html"

    @staticmethod
    def from_string(value: str) -> "TemplateType":
        return next((t for t in TemplateType if t.value == value), TemplateType.PAGE)

@dataclass
class Post:
    title: str
    date: str
    html_content: str
    slug: str
    template: TemplateType = TemplateType.POST

@dataclass
class Page:
    title: str
    date: str
    description: str
    slug: str
    template: TemplateType
