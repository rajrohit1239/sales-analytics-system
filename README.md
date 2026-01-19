# Sales Analytics System

## Overview
This Python-based system processes sales transaction data, cleanses it, enriches it with external product data from a public API, and generates comprehensive business reports. It is designed to handle large datasets, manage encoding issues, and provide actionable insights like top-selling products and regional performance.

## Project Structure
```text
sales-analytics-system/
│
├── data/
│   ├── sales_data.txt          # Raw input data
│   └── enriched_sales_data.txt # (Generated) Enriched output data
│
├── output/
│   └── sales_report.txt        # (Generated) Final business report
│
├── utils/
│   ├── file_handler.py         # Reads/Writes files
│   ├── data_processor.py       # Cleans, filters, and analyzes data
│   └── api_handler.py          # Fetches data from DummyJSON API
│
├── main.py                     # Main execution script
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation