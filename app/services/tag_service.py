from typing import List
from models.tag import Tag, TagShortView

tag_collection = Tag


async def add_tag(new_tag: Tag) -> Tag:
    tag = await new_tag.insert()
    return tag


async def get_all_tag() -> List[Tag]:
    tags = await tag_collection.find().project(TagShortView).to_list()
    return tags