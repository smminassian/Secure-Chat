from aiosqlite import Connection, Row, connect, IntegrityError
from typing import Iterable
from models import User
# from random import randint

DATABASE_URL = "main.db"

async def get_user(db: Connection, username: str) -> Row | None:

    async with db.execute("SELECT * FROM User WHERE username = ?", (username,)) as cursor:
        user = await cursor.fetchone()
        return user


async def create_user(db: Connection, username: str, password: str) -> Row | None:
    # TODO: 
    # - Hash password
    # - Check if username already exists
    # - Return user object

    # Make sure username doesnt already exist
    if await get_user(db, username):
        return None
    
    try:
        await db.execute(
            "INSERT INTO User (username, password) VALUES (?, ?)", 
            (username, password)
        )
        await db.commit()
    except IntegrityError:
        return None

    return await get_user(db, username)

async def users_in(db: Connection, chat_id: int) -> Iterable[Row]:
    async with db.execute("""
    SELECT username FROM User
    JOIN InChat ON User.ID = InChat.user_id
    WHERE chat_id = ?
    """, (chat_id,)) as cursor:
        return await cursor.fetchall()


        # CREATE TABLE IF NOT EXISTS Session (
        #     session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     user_id INTEGER,
        #     last_seen TIMESTAMP,
        #     status TEXT,
        #     device TEXT,
        #     ip_address TEXT,
        #     FOREIGN KEY (user_id) REFERENCES User(ID)


async def create_session(db:Connection, user: User):

    async with db.execute("INSERT INTO Session (user_id) VALUES (?)", (user.ID,)) as cursor:
        
        await cursor.commit()

    # Store session information in map
    # Session should store:
    # user that is logged in
    # When logged in ??
    # When it expires??


# # Change this when sessions are figured out.
async def get_session(db: Connection, session_id: str) -> Row | None:

    async with db.execute("SELECT * FROM Session WHERE session_id = ?", (session_id,)) as cursor:
        session = await cursor.fetchone()
        # logging maybe?
        return session 

async def get_session_username(db: Connection, username: str) -> Row | None:
    query = """
        SELECT Session.*, User.username 
        FROM Session
        JOIN User ON Session.user_id = User.ID
        WHERE User.username = ?
    """

    async with db.execute(query, (username,)) as cursor:
        session = await cursor.fetchone()
        # logging maybe?
        return session


# def session_exists(username: str):
#     for _, sesh in sessions.items():
#         if sesh == username:
#             return True
#     return False


# def user_in(chat_id: str):
#     # Get a list of all usernames that are a part of the chat
#     pass


async def init_db():
    async with connect(DATABASE_URL) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS User (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS Chat (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS InChat (
            user_id INTEGER,
            chat_id INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, chat_id),
            FOREIGN KEY (user_id) REFERENCES User(ID),
            FOREIGN KEY (chat_id) REFERENCES Chat(ID)
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS Friendship (
            P1 INTEGER,
            P2 INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (P1, P2),
            FOREIGN KEY (P1) REFERENCES User(ID),
            FOREIGN KEY (P2) REFERENCES User(ID)
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS Message (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            sent_by INTEGER,
            chat_id INTEGER,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_read BOOLEAN DEFAULT 0,
            FOREIGN KEY (sent_by) REFERENCES User(ID),
            FOREIGN KEY (chat_id) REFERENCES Chat(ID)
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS Session (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            last_seen TIMESTAMP,
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES User(ID)
        )
        """)

        await db.commit()
        print("Database initialized successfully!")
