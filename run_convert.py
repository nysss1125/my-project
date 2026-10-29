import glob, os, pdfplumber

pdf_files = glob.glob('*.pdf') + glob.glob('**/*.pdf', recursive=True)
for f in pdf_files:
    if '.github' in f: continue
    try:
        with pdfplumber.open(f) as pdf:
            txts = [p.extract_text() for p in pdf.pages if p.extract_text()]
        out = os.path.splitext(f)[0] + '.md'
        with open(out, 'w', encoding='utf-8') as fp:
            fp.write('\n\n---\n\n'.join(txts))
        print(f'Done: {f}')
    except Exception as e:
        print(f'Error {f}: {e}')
