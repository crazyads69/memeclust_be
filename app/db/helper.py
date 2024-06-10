from supabase import Client, create_client
import supabase, os


class DBHelper:
    # Init the supabase client
    def __init__(self) -> None:
        pass

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass


class Supabase:
    def __init__(self) -> None:
        pass

    def create_client(self) -> Client:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE")
        if supabase_url is None or supabase_key is None:
            raise Exception("Supabase URL or Key is not set")
        supabase = create_client(supabase_url=supabase_url, supabase_key=supabase_key)
        return supabase
