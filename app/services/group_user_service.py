from typing import List

from models.group_user import GroupUser, GroupUserShortView
from models.roles import Roles, RolesShortVIew

group_user_collection = GroupUser
roles_collection = Roles


async def retrieve_all_group_user() -> List[GroupUserShortView]:
    roles = await roles_collection.find({"permissions": "view_alert"}).project(RolesShortVIew).to_list()
    if roles:
        list_role_id = []
        for role in roles:
            list_role_id.append(role.role_id)
        groups = await group_user_collection.find(
            {"active": True, "role": {"$in": list_role_id}}).project(GroupUserShortView).to_list()
        if groups:
            return groups
