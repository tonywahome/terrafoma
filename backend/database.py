from supabase import create_client, Client
from config import settings


def get_supabase_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_anon_key)


def get_admin_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_service_role_key)
