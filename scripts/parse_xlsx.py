import zipfile
import xml.etree.ElementTree as ET
import sys
import json
import os

def parse_xlsx(file_path):
    if not os.path.exists(file_path):
        return None
    
    with zipfile.ZipFile(file_path, 'r') as z:
        # Load shared strings
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
            # namespace handled by finding text tags
            for elem in tree.iter():
                if elem.tag.endswith('t'):
                    if elem.text:
                        shared_strings.append(elem.text)
                    else:
                        shared_strings.append("")

        # Read sheet1.xml
        sheet_tree = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        rows_data = []
        
        # Find sheetData
        sheet_data = None
        for child in sheet_tree:
            if child.tag.endswith('sheetData'):
                sheet_data = child
                break
        
        if not sheet_data:
            return []

        for row_elem in sheet_data:
            row = []
            for cell_elem in row_elem:
                val_type = cell_elem.attrib.get('t')
                val = ""
                for child in cell_elem:
                    if child.tag.endswith('v'):
                        val = child.text
                        break
                
                if val_type == 's' and val != "":
                    idx = int(val)
                    if idx < len(shared_strings):
                        val = shared_strings[idx]
                row.append(val)
            if any(cell != "" and cell is not None for cell in row):
                rows_data.append(row)
                
        return rows_data

if __name__ == "__main__":
    files = ['Banks related.xlsx', 'IT Related.xlsx', 'healthcare related.xlsx']
    result = {}
    for f in files:
        data = parse_xlsx(f)
        if data:
            result[f] = data
            print(f"=== {f} ({len(data)} rows) ===")
            for r in data[:5]:
                print(r)
            print()
    with open('parsed_xlsx.json', 'w', encoding='utf8') as out:
        json.dump(result, out, indent=2, ensure_ascii=False)
