def read_sales_data(filename):
    """
    This function opens the file and reads the lines.
    It ignores the header (the first line) and any empty lines.
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for code in encodings:
        try:
            with open(filename, 'r', encoding=code) as file:
                lines = file.readlines()
                
                if not lines:
                    return []
                data_lines = lines[1:]
                clean_lines = []
                for line in data_lines:
                    if line.strip(): 
                        clean_lines.append(line.strip())
                return clean_lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: Could not find the file at {filename}")
            return []

    return []


# ... Part 3.2 ...

def save_enriched_data(enriched_transactions, filename):
    """
    Saves the enriched data to a pipe-delimited text file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
            file.write(header)
            
            for t in enriched_transactions:
                line = (
                    f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|{t['ProductName']}|"
                    f"{t['Quantity']}|{t['UnitPrice']}|{t['CustomerID']}|{t['Region']}|"
                    f"{t['API_Category']}|{t['API_Brand']}|{t['API_Rating']}|{t['API_Match']}\n"
                )
                file.write(line)
                
        print(f"Successfully saved {len(enriched_transactions)} records to {filename}")
        return True
        
    except IOError as e:
        print(f"Error saving file: {e}")
        return False