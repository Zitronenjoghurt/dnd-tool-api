from database import MongoDB, get_db
from models.entities.user import User


async def setup_database():
    db = await get_db()
    await create_unique_keys(db)

async def create_unique_keys(db: MongoDB):
    await db.create_unique_index(User.collection_name(), 'username')
    await db.create_unique_index(User.collection_name(), 'email')