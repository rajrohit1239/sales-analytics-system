def parse_transactions(raw_lines):
    """
    Parses raw strings into a clean list of dictionaries.
    Applies data cleaning rules (removes commas, checks types).
    """
    valid_transactions = []
    
    for line in raw_lines:
        parts = line.split('|')
        if len(parts) != 8:
            continue
        trans_id = parts[0]
        date = parts[1]
        prod_id = parts[2]
        prod_name = parts[3]
        qty_str = parts[4]
        price_str = parts[5]
        cust_id = parts[6]
        region = parts[7]
        
        if not trans_id.startswith('T'):
            continue
            
        if not cust_id or not region:
            continue
            
        clean_prod_name = prod_name.replace(',', '')
        
        try:
            clean_qty_str = qty_str.replace(',', '')
            clean_price_str = price_str.replace(',', '')
            
            quantity = int(clean_qty_str)
            unit_price = float(clean_price_str)
            
            if quantity <= 0 or unit_price <= 0:
                continue
                
        except ValueError:
            continue
            
        transaction = {
            'TransactionID': trans_id,
            'Date': date,
            'ProductID': prod_id,
            'ProductName': clean_prod_name,
            'Quantity': quantity,
            'UnitPrice': unit_price, 
            'CustomerID': cust_id,
            'Region': region
        }
        
        valid_transactions.append(transaction)
        
    return valid_transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters (Region and Amount).
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """
    valid_filtered_transactions = []
    invalid_count = 0
    
    
    dropped_by_region = 0
    dropped_by_amount = 0
    
    
    all_regions = sorted(list(set(t['Region'] for t in transactions if t.get('Region'))))
    all_amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
    
    print("\n--- Filter Options Available ---")
    print(f"Regions found: {all_regions}")
    if all_amounts:
        print(f"Transaction Amounts range: {min(all_amounts)} to {max(all_amounts)}")
    
    
    for t in transactions:
        
       
        if (not t['TransactionID'].startswith('T') or
            not t['ProductID'].startswith('P') or
            not t['CustomerID'].startswith('C') or
            t['Quantity'] <= 0 or 
            t['UnitPrice'] <= 0):
            
            invalid_count += 1
            continue 

      
        if region and t['Region'] != region:
            dropped_by_region += 1
            continue

        
        total_amount = t['Quantity'] * t['UnitPrice']

        if min_amount is not None and total_amount < min_amount:
            dropped_by_amount += 1
            continue
        if max_amount is not None and total_amount > max_amount:
            dropped_by_amount += 1
            continue

        valid_filtered_transactions.append(t)

    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': dropped_by_region,
        'filtered_by_amount': dropped_by_amount,
        'final_count': len(valid_filtered_transactions)
    }

    return valid_filtered_transactions, invalid_count, filter_summary

# ... Part 2(a)...

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    Returns: float (total revenue)
    """
    total_revenue = 0.0
    
    for t in transactions:
        
        amount = t['Quantity'] * t['UnitPrice']
        
        
        total_revenue += amount
        
    return total_revenue

# ... Part 2(b) ...

def region_wise_sales(transactions):
    """
    Analyzes sales by region.
    Returns: dictionary with region statistics, sorted by total sales (descending).
    """
    
    region_stats = {}
    total_revenue_all = 0.0

    
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']
        
        
        total_revenue_all += amount

        
        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}
        
        
        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1

    
    final_stats = {}
    
    
    sorted_regions = sorted(region_stats, key=lambda r: region_stats[r]['total_sales'], reverse=True)

    for region in sorted_regions:
        data = region_stats[region]
        sales = data['total_sales']
        count = data['transaction_count']
        
        
        if total_revenue_all > 0:
            percentage = (sales / total_revenue_all) * 100
        else:
            percentage = 0.0
            
        
        final_stats[region] = {
            'total_sales': sales,
            'transaction_count': count,
            'percentage': round(percentage, 2)
        }
        
    return final_stats

# ... Part 2(c) ...

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_stats = {}

    for t in transactions:
        prod_name = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']

        if prod_name not in product_stats:
            product_stats[prod_name] = {'total_qty': 0, 'total_revenue': 0.0}

        product_stats[prod_name]['total_qty'] += qty
        product_stats[prod_name]['total_revenue'] += revenue

    product_list = []
    for name, stats in product_stats.items():
        product_list.append((name, stats['total_qty'], stats['total_revenue']))

    sorted_products = sorted(product_list, key=lambda x: x[1], reverse=True)

    return sorted_products[:n]

# ... Part 2(d) ...

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    Returns: dictionary of customer statistics, sorted by total spent (descending).
    """
    customer_stats = {}

    for t in transactions:
        cust_id = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        prod_name = t['ProductName']

        if cust_id not in customer_stats:
            customer_stats[cust_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set() 
            }

        customer_stats[cust_id]['total_spent'] += amount
        customer_stats[cust_id]['purchase_count'] += 1
        customer_stats[cust_id]['products_bought'].add(prod_name)

    final_stats = {}
    
    sorted_customers = sorted(customer_stats, key=lambda c: customer_stats[c]['total_spent'], reverse=True)

    for cust_id in sorted_customers:
        data = customer_stats[cust_id]
        spent = data['total_spent']
        count = data['purchase_count']
        
        avg_value = spent / count if count > 0 else 0.0
        
        products_list = list(data['products_bought'])

        final_stats[cust_id] = {
            'total_spent': spent,
            'purchase_count': count,
            'avg_order_value': round(avg_value, 2),
            'products_bought': products_list
        }

    return final_stats


# ... Part 2.2(a) ...

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    Returns: dictionary sorted by date with revenue, count, and unique customers.
    """
    daily_stats = {}

    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        cust_id = t['CustomerID']

        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers_set': set() 
            }

        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['unique_customers_set'].add(cust_id)

    final_stats = {}
    
    sorted_dates = sorted(daily_stats.keys())

    for date in sorted_dates:
        data = daily_stats[date]
        
        final_stats[date] = {
            'revenue': data['revenue'],
            'transaction_count': data['transaction_count'],
            'unique_customers': len(data['unique_customers_set']) 
        }

    return final_stats

# ... Part 2.2(b) ...

def find_peak_sales_day(transactions):
    """
    Identifies the date with the highest revenue.
    Returns: tuple (date, revenue, transaction_count)
    """
    daily_stats = daily_sales_trend(transactions)
    
    peak_date = None
    max_revenue = -1.0
    peak_count = 0
    
    for date, data in daily_stats.items():
        if data['revenue'] > max_revenue:
            max_revenue = data['revenue']
            peak_date = date
            peak_count = data['transaction_count']
            
    return (peak_date, max_revenue, peak_count)


# ... Part 2.3(a) ...

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with sales quantity below a threshold.
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue) sorted by quantity (ascending).
    """
    product_stats = {}

    for t in transactions:
        prod_name = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']

        if prod_name not in product_stats:
            product_stats[prod_name] = {'total_qty': 0, 'total_revenue': 0.0}

        product_stats[prod_name]['total_qty'] += qty
        product_stats[prod_name]['total_revenue'] += revenue

    low_performers = []
    
    for name, stats in product_stats.items():
        if stats['total_qty'] < threshold:
            low_performers.append((name, stats['total_qty'], stats['total_revenue']))

    sorted_low_performers = sorted(low_performers, key=lambda x: x[1])

    return sorted_low_performers


# ... Part 3.2 ...

def enrich_sales_data(transactions, product_mapping):
    """
    Merges local sales data with API product details.
    """
    enriched_data = []
    
    for t in transactions:
        enriched_t = t.copy()
        
        raw_prod_id = t['ProductID']
        product_id = None
        
        try:
            if raw_prod_id.startswith('P'):
                product_id = int(raw_prod_id[1:])
            else:
                product_id = int(raw_prod_id)
        except ValueError:
            product_id = None

        if product_id and product_id in product_mapping:
            api_data = product_mapping[product_id]
            
            enriched_t['API_Category'] = api_data.get('category')
            enriched_t['API_Brand'] = api_data.get('brand')
            enriched_t['API_Rating'] = api_data.get('rating')
            enriched_t['API_Match'] = True
        else:
            enriched_t['API_Category'] = "N/A"
            enriched_t['API_Brand'] = "N/A"
            enriched_t['API_Rating'] = "N/A"
            enriched_t['API_Match'] = False
            
        enriched_data.append(enriched_t)
        
    return enriched_data


# ... Part 4.1 ...

import datetime
import os

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive text report with all analysis metrics.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    total_revenue = calculate_total_revenue(transactions)
    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, n=5)
    customer_stats = customer_analysis(transactions)
    daily_stats = daily_sales_trend(transactions)
    peak_day_date, peak_day_rev, peak_day_trans = find_peak_sales_day(transactions)
    low_performers = low_performing_products(transactions, threshold=5) 
    
    total_trans = len(transactions)
    avg_order_val = total_revenue / total_trans if total_trans > 0 else 0
    
    dates = sorted([t['Date'] for t in transactions])
    start_date = dates[0] if dates else "N/A"
    end_date = dates[-1] if dates else "N/A"

    total_enriched = len(enriched_transactions)
    successful_matches = sum(1 for t in enriched_transactions if t.get('API_Match'))
    success_rate = (successful_matches / total_enriched * 100) if total_enriched > 0 else 0.0
    
    failed_products = set()
    for t in enriched_transactions:
        if not t.get('API_Match'):
            failed_products.add(t['ProductID'])

    lines = []
    
    lines.append("=" * 60)
    lines.append("              SALES ANALYTICS REPORT")
    lines.append(f"          Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"          Records Processed: {total_trans}")
    lines.append("=" * 60)
    lines.append("\n")

    lines.append("1. OVERALL SUMMARY")
    lines.append("-" * 60)
    lines.append(f"Total Revenue:       ${total_revenue:,.2f}")
    lines.append(f"Total Transactions:  {total_trans}")
    lines.append(f"Average Order Value: ${avg_order_val:,.2f}")
    lines.append(f"Date Range:          {start_date} to {end_date}")
    lines.append("\n")

    lines.append("2. REGION-WISE PERFORMANCE")
    lines.append("-" * 60)
    lines.append(f"{'Region':<15} | {'Sales':<15} | {'% Total':<10} | {'Trans':<5}")
    lines.append("-" * 60)
    for region, data in region_stats.items():
        lines.append(f"{region:<15} | ${data['total_sales']:<14,.2f} | {data['percentage']:<9}% | {data['transaction_count']:<5}")
    lines.append("\n")

    lines.append("3. TOP 5 PRODUCTS")
    lines.append("-" * 60)
    lines.append(f"{'Rank':<5} | {'Product':<25} | {'Qty':<5} | {'Revenue':<15}")
    lines.append("-" * 60)
    for idx, (name, qty, rev) in enumerate(top_products, 1):
        lines.append(f"{idx:<5} | {name:<25} | {qty:<5} | ${rev:<14,.2f}")
    lines.append("\n")

    lines.append("4. TOP 5 CUSTOMERS")
    lines.append("-" * 60)
    lines.append(f"{'Rank':<5} | {'Customer ID':<15} | {'Total Spent':<15} | {'Orders':<5}")
    lines.append("-" * 60)
    sorted_customers = sorted(customer_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True)[:5]
    for idx, (cust_id, data) in enumerate(sorted_customers, 1):
        lines.append(f"{idx:<5} | {cust_id:<15} | ${data['total_spent']:<14,.2f} | {data['purchase_count']:<5}")
    lines.append("\n")

    lines.append("5. DAILY SALES TREND")
    lines.append("-" * 60)
    lines.append(f"{'Date':<15} | {'Revenue':<15} | {'Trans':<5} | {'Unique Cust':<10}")
    lines.append("-" * 60)
    for date, data in daily_stats.items():
        lines.append(f"{date:<15} | ${data['revenue']:<14,.2f} | {data['transaction_count']:<5} | {data['unique_customers']:<10}")
    lines.append("\n")

    lines.append("6. PRODUCT PERFORMANCE ANALYSIS")
    lines.append("-" * 60)
    lines.append(f"Best Selling Day: {peak_day_date} (${peak_day_rev:,.2f} with {peak_day_trans} orders)")
    if low_performers:
        lines.append("\nLow Performing Products (Warning: Check Inventory):")
        for name, qty, rev in low_performers:
            lines.append(f" - {name} (Qty: {qty}, Rev: ${rev:,.2f})")
    else:
        lines.append("\nNo products are performing below threshold.")
    lines.append("\n")

    lines.append("7. API ENRICHMENT SUMMARY")
    lines.append("-" * 60)
    lines.append(f"Total Records Enriched: {total_enriched}")
    lines.append(f"Successful API Matches: {successful_matches}")
    lines.append(f"Success Rate:           {success_rate:.2f}%")
    if failed_products:
        lines.append(f"Failed to Match Product IDs: {', '.join(map(str, list(failed_products)[:10]))}...")
    lines.append("\n")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"\n[SUCCESS] Report generated successfully at: {output_file}")
        return True
    except IOError as e:
        print(f"\n[ERROR] Could not write report: {e}")
        return False