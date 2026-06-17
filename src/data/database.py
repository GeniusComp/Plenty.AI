import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client.
    This is the single connection point to our database.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Missing Supabase credentials in .env file")
    
    return create_client(url, key)


def save_prices(products: list, search_term: str) -> bool:
    """
    Saves a list of products to the price_cache table.
    
    Args:
        products: List of product dictionaries from the Walmart agent
        search_term: The search term used to find these products
    
    Returns:
        True if successful, False if failed
    """
    try:
        client = get_supabase_client()
        
        records = []
        for product in products:
            record = {
                "product_name": product.get("name", "Unknown"),
                "search_term": search_term,
                "store": "walmart",
                "price": str(product.get("price", "")),
                "unit_price": str(product.get("unit_price", "")),
                "availability": product.get("available", "Unknown")
            }
            records.append(record)
        
        result = client.table("price_cache").insert(records).execute()
        
        print(f"Saved {len(records)} products to database for '{search_term}'")
        return True
        
    except Exception as e:
        print(f"Database error: {e}")
        return False


def get_cached_prices(search_term: str) -> list:
    """
    Retrieves cached prices for a search term from the last 4 hours.
    
    Args:
        search_term: The grocery item to look up
    
    Returns:
        List of cached price records
    """
    try:
        client = get_supabase_client()
        
        result = client.table("price_cache")\
            .select("*")\
            .eq("search_term", search_term)\
            .order("fetched_at", desc=True)\
            .limit(10)\
            .execute()
        
        return result.data
        
    except Exception as e:
        print(f"Database retrieval error: {e}")
        return []