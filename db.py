import asyncpg
from datetime import datetime

pool = None

async def create_pool():
    global pool
    print('Creating pool')
    pool = await asyncpg.create_pool(
        user='postgres',
        password='QwEr0101',
        database='postgres',
        host='localhost',
        port='5432'
    )

async def get_connection():
    if pool is None:
        await create_pool()
    return pool

async def get_user_by_id(user_id):
    try:
        conn = await get_connection()
        async with conn.acquire() as connection:
            return await connection.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)
    except Exception as e:
        print('Error in get_user_by_id:', e)
        return None
    
async def create_or_get_user(user_id, username, first_name, last_name, lang_code):
    try:
        conn = await get_connection()
        async with conn.acquire() as connection:
            user = await connection.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)
            if not user:
                if lang_code not in ("ru", "kz"):
                    lang_code = "kz"
                await connection.execute('''
                    INSERT INTO users (user_id, username, name, surname, language)
                    VALUES ($1, $2, $3, $4, $5)
                ''', user_id, username, first_name, last_name, lang_code)
                user = await connection.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)
            return user
    except Exception as e:
        print('Error in create_or_get_user:', e)
        return None