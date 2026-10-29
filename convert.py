import glob
import os
import pdfplumber

# 搜尋根目錄與子目錄下所有 PDF 檔案
pdf_files = glob.glob('*.pdf') + glob.glob('**/*.pdf', recursive=True)

for pdf_file in pdf_files:
    # 忽略隱藏資料夾裡的檔名
    if '.github' in pdf_file:
        continue

    try:
        with pdfplumber.open(pdf_file) as pdf:
            pages_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
            full_text = '\n\n---\n\n'.join(pages_text)

        md_filename = os.path.splitext(pdf_file)[0] + '.md'
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f'Successfully converted: {pdf_file} -> {md_filename}')
    except Exception as e:
        print(f'Error processing {pdf_file}: {e}')
