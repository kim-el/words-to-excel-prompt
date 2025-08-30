#!/usr/bin/env python3
"""
Convert Word document tables to Excel file
"""

import pandas as pd
from docx import Document
import sys
import os

def extract_tables_from_word(word_file_path):
    """
    Extract all tables from a Word document
    """
    try:
        # Open the Word document
        doc = Document(word_file_path)
        
        all_tables_data = []
        
        # Process each table in the document
        for table_num, table in enumerate(doc.tables, 1):
            print(f"Processing table {table_num}...")
            
            table_data = []
            
            # Extract each row
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    # Clean up cell text
                    cell_text = cell.text.strip()
                    row_data.append(cell_text)
                table_data.append(row_data)
            
            if table_data:
                # Create DataFrame for this table
                df = pd.DataFrame(table_data)
                
                # Use first row as headers if it looks like headers
                if len(table_data) > 1:
                    # Check if first row has non-empty values that could be headers
                    first_row = table_data[0]
                    if any(cell.strip() for cell in first_row):
                        df.columns = first_row
                        df = df.iloc[1:].reset_index(drop=True)
                
                all_tables_data.append({
                    'table_number': table_num,
                    'dataframe': df,
                    'raw_data': table_data
                })
        
        return all_tables_data
    
    except Exception as e:
        print(f"Error reading Word file: {e}")
        return None

def save_tables_to_excel(tables_data, output_file):
    """
    Save extracted tables to Excel file
    """
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for table_info in tables_data:
                sheet_name = f"Table_{table_info['table_number']}"
                df = table_info['dataframe']
                
                # Save to Excel
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Saved {sheet_name} with {len(df)} rows and {len(df.columns)} columns")
        
        print(f"\n✅ Successfully saved {len(tables_data)} tables to {output_file}")
        return True
    
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        return False

def main():
    # Input and output file paths
    word_file = "/Users/kimen/Downloads/Untitled document.docx"
    excel_file = "/Users/kimen/Projects/Zendesk-Tickets-Test/word_tables_output.xlsx"
    
    # Check if input file exists
    if not os.path.exists(word_file):
        print(f"❌ Input file not found: {word_file}")
        return
    
    print(f"📖 Reading Word file: {word_file}")
    
    # Extract tables from Word document
    tables_data = extract_tables_from_word(word_file)
    
    if not tables_data:
        print("❌ No tables found or error occurred")
        return
    
    print(f"📊 Found {len(tables_data)} tables")
    
    # Save to Excel
    if save_tables_to_excel(tables_data, excel_file):
        # Show preview of first table
        if tables_data:
            print(f"\n📋 Preview of first table:")
            print(tables_data[0]['dataframe'].head())
            
        print(f"\n🎉 Output saved to: {excel_file}")
    else:
        print("❌ Failed to save Excel file")

if __name__ == "__main__":
    main()