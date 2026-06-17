import os
import requests
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.data.database import save_prices
# Load environment variables from .env file
load_dotenv()

# Get our RapidAPI key from the environment
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def search_walmart_products(query: str, limit: int = 5) -> list:
    """
    Search for products on Walmart and return pricing data.
    
    Args:
        query: The product to search for (e.g. "chicken breast")
        limit: How many results to return
    
    Returns:
        A list of products with names and prices
    """
    
    url = "https://axesso-walmart-data-service.p.rapidapi.com/wlm/walmart-search-by-keyword"
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "axesso-walmart-data-service.p.rapidapi.com"
    }
    
    params = {
        "keyword": query,
        "page": "1",
        "sortBy": "best_match"
    }
    
    print(f"Searching Walmart for: {query}")
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []
    
    data = response.json()
    
    products = []
    
    items = data.get("item", {}).get("props", {}).get("pageProps", {}).get("initialData", {}).get("searchResult", {}).get("itemStacks", [{}])[0].get("items", [])
    
    for item in items[:limit]:
        product = {
            "name": item.get("name", "Unknown"),
            "price": item.get("priceInfo", {}).get("linePrice") or item.get("price", "N/A"),
            "unit_price": item.get("priceInfo", {}).get("unitPrice", "N/A"),
            "available": item.get("availabilityStatusDisplayValue", "Unknown")
        }
        products.append(product)
    
    return products


def main():
    """
    Test the Walmart agent with three grocery items.
    This is your first Python agent running in production.
    """
    
    test_items = ["chicken breast", "wheat bread", "maple syrup"]
    
    print("=" * 50)
    print("PLENTY.AI — Walmart Price Agent")
    print("=" * 50)
    
    for item in test_items:
        print(f"\nSearching for: {item.upper()}")
        print("-" * 30)
        
        products = search_walmart_products(item, limit=3)
        if products:
            save_prices(products, item)
        
        if not products:
            print("No results found")
            continue
            
        for i, product in enumerate(products, 1):
            print(f"{i}. {product['name']}")
            print(f"   Price: {product['price']}")
            print(f"   Unit Price: {product['unit_price']}")
            print(f"   Available: {product['available']}")
    
    print("\n" + "=" * 50)
    print("Agent run complete")
    print("=" * 50)


if __name__ == "__main__":
    main()
  
 

