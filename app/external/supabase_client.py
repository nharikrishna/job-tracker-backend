from supabase import create_client
import app.core.config as config

settings = config.get_settings()

supabase = create_client(settings.supabase_url, settings.supabase_key)
