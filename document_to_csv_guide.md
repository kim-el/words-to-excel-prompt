# Document to CSV Conversion Guide

## Step-by-Step Process for Converting Pages/Word Documents to CSV

### Phase 1: Setup Environment

1. **Create virtual environment**
   ```bash
   python3 -m venv doc_converter_env
   source doc_converter_env/bin/activate
   ```

2. **Install required packages**
   ```bash
   pip install pandas python-docx openpyxl
   ```

### Phase 2: Convert Pages Files (if applicable)

3. **Convert Pages to DOCX using AppleScript**
   ```bash
   osascript -e '
   tell application "Pages"
       open POSIX file "/path/to/input.pages"
       tell front document
           export to POSIX file "/path/to/output.docx" as Microsoft Word
           close
       end tell
       quit
   end tell'
   ```

### Phase 3: Extract Content from DOCX

4. **Extract tables and text with structure preservation**
   Create Python script:
   ```python
   import pandas as pd
   from docx import Document
   
   def extract_tables_from_word(word_file_path):
       doc = Document(word_file_path)
       all_tables_data = []
       
       for table_num, table in enumerate(doc.tables, 1):
           print(f"Processing table {table_num}...")
           table_data = []
           
           for row in table.rows:
               row_data = []
               for cell in row.cells:
                   cell_text = cell.text.strip()
                   row_data.append(cell_text)
               table_data.append(row_data)
           
           if table_data:
               df = pd.DataFrame(table_data)
               all_tables_data.append({
                   'table_number': table_num,
                   'dataframe': df
               })
       
       return all_tables_data
   
   def save_tables_to_csv(tables_data, output_prefix):
       for table_info in tables_data:
           table_num = table_info['table_number']
           df = table_info['dataframe']
           output_file = f"{output_prefix}_table_{table_num}.csv"
           df.to_csv(output_file, index=False, header=False)
           print(f"Saved {output_file}")
   
   # Usage
   word_file = "input.docx"
   tables = extract_tables_from_word(word_file)
   save_tables_to_csv(tables, "output")
   ```

5. **Run the extraction script**
   ```bash
   source doc_converter_env/bin/activate
   python extract_tables.py
   ```

### Phase 4: Verify Results

6. **Check output files**
   ```bash
   ls -la *.csv
   head -5 output_table_1.csv
   ```

7. **Read CSV with tools**
   - Now you can use text-based tools to read/edit the CSV files
   - Table structure is preserved with proper rows and columns

### Quick Command Summary

**For Pages → CSV:**
```bash
# 1. Convert Pages to DOCX
osascript -e 'tell application "Pages" to open POSIX file "/path/input.pages"; tell front document to export to POSIX file "/path/output.docx" as Microsoft Word; close; quit'

# 2. Extract tables to CSV
source doc_converter_env/bin/activate
python extract_tables.py
```

**For DOCX → CSV:**
```bash
# Skip step 1, go directly to extraction
source doc_converter_env/bin/activate
python extract_tables.py
```

### Troubleshooting

- **"Excel not defined" error**: Use `Microsoft Word` instead of `Excel` in AppleScript
- **Empty extraction**: Document might have no tables, only paragraphs
- **Permission denied**: Make sure Pages app can be automated in System Preferences
- **Virtual environment issues**: Always activate environment before running Python scripts

### File Types Supported

✅ **Supported:**
- .pages → DOCX → CSV
- .docx → CSV
- .doc → CSV (if converted to .docx first)

❌ **Not directly supported:**
- .pdf (requires different tools)
- .xlsx (use pandas directly)
- .pages → CSV (requires conversion step)