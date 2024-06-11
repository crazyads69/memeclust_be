from supabase import Client, create_client
import supabase, os
from sqlalchemy import Connection, Engine, create_engine


class DBHelper:
    def connect(self) -> Connection:
        db_url = os.getenv("DATABASE_URL")
        if db_url is None:
            raise Exception("Database URL is not set")
        engine = create_engine(
            db_url,
            pool_size=20,
            max_overflow=15,
        )
        return engine.connect()
