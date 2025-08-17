from services.db import DatabaseService
import asyncio

async def init_database():
    """
    Initialize the database with required tables
    """
    db_service = DatabaseService()
    await db_service._create_tables()
    print("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init_database())
