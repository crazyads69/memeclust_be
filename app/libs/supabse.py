from supabase import Client, create_client
import os


class Supabase:
    def create_client(self) -> Client:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE")
        if supabase_url is None or supabase_key is None:
            raise Exception("Supabase URL or Key is not set")
        supabase = create_client(supabase_url=supabase_url, supabase_key=supabase_key)
        return supabase
