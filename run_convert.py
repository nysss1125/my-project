import glob, os, pdfplumber
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract

pdf_files = glob.glob('*.pdf') + glob.glob('**/*.pdf', recursive=True)
for f in pdf_files:
    if '.github' in f: continue
    print(f"=== 開始處理檔案: {f} ===")
    txts = []
    
    # 第一階段：嘗試快速文字層提取 (pdfplumber)
    try:
        with pdfplumber.open(f) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t and len(t.strip()) > 20: # 確保有實質內文
                    txts.append(t.strip())
    except Exception as e:
        print(f"pdfplumber 讀取失敗: {e}")

    # 第二階段：若文字層提取不足，改用 pypdf 備用提取
    if not txts:
        try:
            reader = PdfReader(f)
            for page in reader.pages:
                t = page.extract_text()
                if t and len(t.strip()) > 20:
                    txts.append(t.strip())
        except Exception as e:
            print(f"pypdf 讀取失敗: {e}")

    # 第三階段：若以上皆無文字，啟用 OCR 全自動影像文字辨識 (支援中英文)
    if not txts:
        print(f"偵測到特殊編碼或掃描頁面，啟動 OCR 光學文字辨識辨識中...")
        try:
            images = convert_from_path(f)
            for i, img in enumerate(images):
                ocr_text = pytesseract.image_to_string(img, lang='chi_tra+eng')
                if ocr_text and ocr_text.strip():
                    txts.append(ocr_text.strip())
                print(f"已完成第 {i+1}/{len(images)} 頁 OCR 辨識")
        except Exception as e:
            print(f"OCR 執行過程失敗: {e}")

    out = os.path.splitext(f)[0] + '.md'
    with open(out, 'w', encoding='utf-8') as fp:
        fp.write('\n\n---\n\n'.join(txts))
    print(f"成功輸出 Markdown: {out} (共轉出 {len(txts)} 頁內容)")
