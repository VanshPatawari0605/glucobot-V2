import re
import io


def extract_pdf_values(file_bytes: bytes):
    try:
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            pages = [p.extract_text() or "" for p in reader.pages]
        except Exception:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            pages = [p.extract_text() or "" for p in reader.pages]

        text = "\n".join(pages)

        if not text.strip():
            return None, "PDF appears to be empty or image-based. Please enter values manually."

        def fv(keyword):
            m = re.search(keyword + r"[\s\S]{0,80}?(\d+\.?\d*)", text, re.I)
            return float(m.group(1)) if m else None

        g    = fv(r"glucose")
        bp   = fv(r"(?:blood\s*pressure|bp\b)")
        ins  = fv(r"insulin")
        bmi  = fv(r"(?:bmi|body\s*mass)")
        age  = fv(r"\bage\b")
        preg = fv(r"pregnanc")
        skin = fv(r"skin")
        dpf  = fv(r"(?:pedigree|dpf\b)")

        found = {
            "glucose":        int(g)        if g    is not None else None,
            "blood_pressure": int(bp)       if bp   is not None else None,
            "insulin":        int(ins)      if ins  is not None else None,
            "bmi":            round(bmi,1)  if bmi  is not None else None,
            "age":            int(age)      if age  is not None else None,
            "pregnancies":    int(preg)     if preg is not None else None,
            "skin_thickness": int(skin)     if skin is not None else None,
            "dpf":            round(dpf,3)  if dpf  is not None else None,
        }

        if not any(v is not None for v in found.values()):
            return None, "Could not find medical values in PDF. Please enter values manually."

        return found, None

    except Exception as e:
        return None, f"Could not read PDF: {str(e)[:80]}"