import sys
from utils.file_handler import read_sales_data, save_enriched_data
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.data_processor import (
    parse_transactions, 
    validate_and_filter, 
    enrich_sales_data, 
    generate_sales_report
)

def main():
    print("==========================================")
    print("          SALES ANALYTICS SYSTEM          ")
    print("==========================================")
    
    try:
        # --- STEP 1: LOAD DATA ---
        print("\n[1/10] Reading sales data...")
        file_path = "data/sales_data.txt"
        raw_data = read_sales_data(file_path)
        if not raw_data:
            print("[FAIL] No data found. Exiting.")
            return
        print(f" ✓ Successfully read {len(raw_data)} transactions")

        # --- STEP 2: PARSE DATA ---
        print("\n[2/10] Parsing and cleaning data...")
        parsed_data = parse_transactions(raw_data)
        print(f" ✓ Parsed {len(parsed_data)} records")

        # --- STEP 3: DISPLAY FILTER OPTIONS ---
        print("\n[3/10] Filter Options Available:")
        # Calculate options to show the user
        regions = sorted(list(set(t['Region'] for t in parsed_data)))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in parsed_data]
        min_amt = min(amounts) if amounts else 0
        max_amt = max(amounts) if amounts else 0
        
        print(f" Regions: {', '.join(regions)}")
        print(f" Amount Range: ${min_amt:,.2f} - ${max_amt:,.2f}")

        # --- STEP 4 & 5: USER INTERACTION ---
        filter_region = None
        filter_min = None
        filter_max = None
        
        user_choice = input("\nDo you want to filter data? (y/n): ").strip().lower()
        
        if user_choice == 'y':
            print("\n--- Enter Filter Criteria (Press Enter to skip) ---")
            
          
            reg_input = input(f"Region ({'/'.join(regions)}): ").strip()
            if reg_input in regions:
                filter_region = reg_input
            
            min_input = input("Min Transaction Amount: ").strip()
            if min_input:
                try:
                    filter_min = float(min_input)
                except ValueError:
                    print(" ! Invalid number, ignoring min amount.")

            max_input = input("Max Transaction Amount: ").strip()
            if max_input:
                try:
                    filter_max = float(max_input)
                except ValueError:
                    print(" ! Invalid number, ignoring max amount.")

        # --- STEP 6: VALIDATE & FILTER ---
        print("\n[4/10] Validating transactions...")
        valid_data, invalid_count, summary = validate_and_filter(
            parsed_data, 
            region=filter_region, 
            min_amount=filter_min, 
            max_amount=filter_max
        )
        print(f" ✓ Valid: {len(valid_data)} | Invalid: {invalid_count}")
        if filter_region or filter_min or filter_max:
             print(f" ✓ Filtered Result: Keeping {len(valid_data)} out of {summary['total_input']} records")

        if not valid_data:
            print("[FAIL] No valid data remaining after filtering. Exiting.")
            return

        # --- STEP 7: ANALYSIS ---
        print("\n[5/10] Analyzing sales data...")
        # (The actual analysis happens inside generate_sales_report, but we acknowledge the step here)
        print(" ✓ Analysis complete")

        # --- STEP 8: API FETCH ---
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        if api_products:
             print(f" ✓ Fetched {len(api_products)} products")
        else:
             print(" ! API fetch failed. Proceeding without enrichment.")

        # --- STEP 9: ENRICHMENT ---
        print("\n[7/10] Enriching sales data...")
        product_map = create_product_mapping(api_products) if api_products else {}
        enriched_data = enrich_sales_data(valid_data, product_map)
        
        matches = sum(1 for t in enriched_data if t.get('API_Match'))
        if len(valid_data) > 0:
            match_rate = (matches / len(valid_data)) * 100
        else:
            match_rate = 0
        print(f" ✓ Enriched {matches}/{len(valid_data)} transactions ({match_rate:.1f}%)")

        # --- STEP 10: SAVE DATA ---
        print("\n[8/10] Saving enriched data...")
        save_success = save_enriched_data(enriched_data, "data/enriched_sales_data.txt")
        if save_success:
            print(" ✓ Saved to: data/enriched_sales_data.txt")

        # --- STEP 11: GENERATE REPORT ---
        print("\n[9/10] Generating report...")
        report_success = generate_sales_report(valid_data, enriched_data, "output/sales_report.txt")
        if report_success:
            print(" ✓ Report saved to: output/sales_report.txt")

        # --- FINAL SUCCESS ---
        print("\n[10/10] Process Complete!")
        print("==========================================")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()