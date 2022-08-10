from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.ti_report import TiReport
from models.history import History
from models.attachment import Attachment
from models.tag import Tag
from models.group_user import GroupUser
from models.roles import Roles
from config import config

print("Creating DB Connector")


async def initiate_database():
    ti_portal = AsyncIOMotorClient(config.get('DATABASE_URL'))
    await init_beanie(database=ti_portal.get_default_database(),
                      document_models=[TiReport, History, Attachment, Tag])
    ti_account = AsyncIOMotorClient(config.get('DATABASE_ACCOUNT'))
    await init_beanie(database=ti_account.get_default_database(),
                      document_models=[GroupUser,Roles])
