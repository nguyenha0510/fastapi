from models.attachment import Attachment

attachment_collection = Attachment


async def add_attachment(new_attachment: Attachment) -> Attachment:
    attachment = await new_attachment.insert()
    return attachment


async def retrieve_attachment(obs_id: str) -> Attachment:
    param = {"parent_id": obs_id}
    attachment = await attachment_collection.find(param).to_list()
    if attachment:
        return attachment
