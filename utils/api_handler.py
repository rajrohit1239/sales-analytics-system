import requests

def fetch_all_products():
    """
    Fetches all available products from the DummyJSON API (limit=100).
    Returns: list of simplified product dictionaries.
    """
    url = "https://dummyjson.com/products?limit=100"
    
    print(f"Connecting to API: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        response.raise_for_status()
        
        data = response.json()
        raw_products = data.get('products', [])
        
        
        if raw_products:
            print(f"Success: Fetched {len(raw_products)} products.")
        else:
            print("Warning: API returned 0 products.")
            
        return raw_products

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []

if __name__ == "__main__":
    products = fetch_all_products()
    if products:
        print("\n--- Sample Product ---")
        print(products[0])


    # ...Part 3.2(b) ...

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    Args:
        api_products (list): List of product dictionaries from the API.
    Returns:
        dict: Mapping where key is Product ID and value is product details.
    """
    mapping = {}
    
    for product in api_products:
        p_id = product.get('id')
        
        details = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }
        
        mapping[p_id] = details
        
    return mapping