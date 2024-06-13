from typing import Generator
from libs.supabse import Supabase


def init_supabase_client() -> Generator:
    supabase = Supabase().create_client()
    yield supabase
