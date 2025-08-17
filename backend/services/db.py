import sqlite3
import asyncio
import aiosqlite
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import os

@dataclass
class Note:
    id: str
    original_text: str
    refined_text: Optional[str]
    filename: str
    created_at: datetime
    updated_at: Optional[datetime]

class DatabaseService:
    def __init__(self, db_path: str = "voiceflow.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """
        Initialize database with required tables
        """
        # Run initialization synchronously first time
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, create task
                asyncio.create_task(self._create_tables())
            else:
                # If not in async context, run it
                loop.run_until_complete(self._create_tables())
        except RuntimeError:
            # No event loop, create one
            asyncio.run(self._create_tables())
    
    async def _create_tables(self):
        """
        Create database tables if they don't exist
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Notes table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    original_text TEXT NOT NULL,
                    refined_text TEXT,
                    filename TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP
                )
            """)
            
            # User preferences table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY,
                    custom_prompt TEXT,
                    default_tone TEXT DEFAULT 'casual',
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP
                )
            """)
            
            # Create indexes for better performance
            await db.execute("CREATE INDEX IF NOT EXISTS idx_notes_created_at ON notes(created_at DESC)")
            
            await db.commit()
    
    async def save_note(
        self, 
        original_text: str, 
        filename: str, 
        created_at: datetime
    ) -> str:
        """
        Save a new note to the database
        """
        note_id = str(uuid.uuid4())
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO notes (id, original_text, filename, created_at)
                VALUES (?, ?, ?, ?)
            """, (note_id, original_text, filename, created_at))
            await db.commit()
        
        return note_id
    
    async def get_note(self, note_id: str) -> Optional[Note]:
        """
        Get a note by ID
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT id, original_text, refined_text, filename, created_at, updated_at
                FROM notes WHERE id = ?
            """, (note_id,)) as cursor:
                row = await cursor.fetchone()
                
                if row:
                    return Note(
                        id=row['id'],
                        original_text=row['original_text'],
                        refined_text=row['refined_text'],
                        filename=row['filename'],
                        created_at=datetime.fromisoformat(row['created_at']),
                        updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
                    )
                return None
    
    async def update_note(self, note_id: str, refined_text: str) -> bool:
        """
        Update a note with refined text
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE notes 
                SET refined_text = ?, updated_at = ?
                WHERE id = ?
            """, (refined_text, datetime.utcnow(), note_id))
            await db.commit()
            
            # Check if update was successful
            async with db.execute("SELECT changes()") as cursor:
                result = await cursor.fetchone()
                return result[0] > 0
    
    async def get_notes(self, limit: int = 20, offset: int = 0) -> List[Note]:
        """
        Get notes with pagination
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT id, original_text, refined_text, filename, created_at, updated_at
                FROM notes 
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (limit, offset)) as cursor:
                rows = await cursor.fetchall()
                
                return [
                    Note(
                        id=row['id'],
                        original_text=row['original_text'],
                        refined_text=row['refined_text'],
                        filename=row['filename'],
                        created_at=datetime.fromisoformat(row['created_at']),
                        updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
                    )
                    for row in rows
                ]
    
    async def get_notes_count(self) -> int:
        """
        Get total count of notes
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM notes") as cursor:
                result = await cursor.fetchone()
                return result[0]
    
    async def delete_note(self, note_id: str) -> bool:
        """
        Delete a note by ID
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            await db.commit()
            
            # Check if deletion was successful
            async with db.execute("SELECT changes()") as cursor:
                result = await cursor.fetchone()
                return result[0] > 0
    
    async def save_user_prompt(self, custom_prompt: str) -> bool:
        """
        Save or update user's custom prompt
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Check if preferences exist
            async with db.execute("SELECT id FROM user_preferences LIMIT 1") as cursor:
                row = await cursor.fetchone()
                
                if row:
                    # Update existing
                    await db.execute("""
                        UPDATE user_preferences 
                        SET custom_prompt = ?, updated_at = ?
                    """, (custom_prompt, datetime.utcnow()))
                else:
                    # Insert new
                    await db.execute("""
                        INSERT INTO user_preferences (custom_prompt, created_at)
                        VALUES (?, ?)
                    """, (custom_prompt, datetime.utcnow()))
                
                await db.commit()
                return True
    
    async def get_user_prompt(self) -> Optional[str]:
        """
        Get user's custom prompt
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT custom_prompt FROM user_preferences LIMIT 1") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None
    
    async def search_notes(self, query: str, limit: int = 20) -> List[Note]:
        """
        Search notes by text content
        """
        search_query = f"%{query}%"
        
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT id, original_text, refined_text, filename, created_at, updated_at
                FROM notes 
                WHERE original_text LIKE ? OR refined_text LIKE ? OR filename LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (search_query, search_query, search_query, limit)) as cursor:
                rows = await cursor.fetchall()
                
                return [
                    Note(
                        id=row['id'],
                        original_text=row['original_text'],
                        refined_text=row['refined_text'],
                        filename=row['filename'],
                        created_at=datetime.fromisoformat(row['created_at']),
                        updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
                    )
                    for row in rows
                ]
