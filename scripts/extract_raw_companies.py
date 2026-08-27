import zipfile, xml.etree.ElementTree as ET, json, os, re

def col2idx(col_str):
    idx = 0
    for char in col_str:
        idx = idx * 26 + (ord(char.upper()) - ord('A')) + 1
    return idx - 1

def extract_rows(file_path):
    if not os.path.exists(file_path):
        return []
    with zipfile.ZipFile(file_path, 'r') as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for elem in tree.iter():
                if elem.tag.endswith('t'):
                    shared_strings.append(elem.text if elem.text else '')

        sheet_tree = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        sheet_data = next((c for c in sheet_tree if c.tag.endswith('sheetData')), None)
        if sheet_data is None:
            return []

        rows_list = []
        for row_elem in sheet_data:
            row_map = {}
            max_col = 0
            for cell_elem in row_elem:
                r_attr = cell_elem.attrib.get('r', '')
                m = re.match(r'([A-Z]+)(\d+)', r_attr)
                if not m:
                    continue
                col_name, _ = m.groups()
                col_idx = col2idx(col_name)
                max_col = max(max_col, col_idx)

                val_type = cell_elem.attrib.get('t')
                val = ''
                for child in cell_elem:
                    if child.tag.endswith('v'):
                        val = child.text if child.text else ''
                        break
                if val_type == 's' and val != '':
                    s_idx = int(val)
                    if s_idx < len(shared_strings):
                        val = shared_strings[s_idx]
                row_map[col_idx] = val

            if row_map:
                row_arr = [row_map.get(i, '').strip() for i in range(max_col + 1)]
                rows_list.append(row_arr)
        return rows_list

banks_rows = extract_rows('Banks related.xlsx')
it_rows = extract_rows('IT Related.xlsx')
health_rows = extract_rows('healthcare related.xlsx')

print(f"Loaded: Banks ({len(banks_rows)}), IT ({len(it_rows)}), Health ({len(health_rows)})")

with open('raw_extracted.json', 'w', encoding='utf8') as f:
    json.dump({
        'banks': banks_rows,
        'it': it_rows,
        'health': health_rows
    }, f, indent=2, ensure_ascii=False)
