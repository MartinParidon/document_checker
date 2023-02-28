from PyPDF2 import PdfReader
import textract


supported_extensions_global = ['pdf', 'doc', 'docx', 'txt']


# Test consolidation of sub functions:
# https://textract.readthedocs.io/en/stable/python_package.html
# text = textract.process('path/to/file.extension')
def get_string_from_path(text_path):
    txt_file_ext = text_path.split('.')[-1]
    if txt_file_ext in supported_extensions_global:
        if (txt_file_ext == 'doc') or (txt_file_ext == 'docx'):
            try:
                full_text_ut = textract.process(text_path).decode("utf8")
                if full_text_ut:
                    return full_text_ut
                else:
                    return None
            except Exception:
                return None
        elif txt_file_ext == 'pdf':
            try:
                reader = PdfReader(text_path)
                full_text_ut = ""
                for page in reader.pages:
                    try:
                        full_text_ut += page.extract_text() + " "
                    except Exception:
                        continue
                if full_text_ut:
                    return full_text_ut
                else:
                    return None
            except Exception:
                return None
        elif txt_file_ext == 'txt':
            try:
                with open(text_path, "r") as text_file:
                    full_text_ut = text_file.read()
                    if full_text_ut:
                        return full_text_ut
                    else:
                        return None
            except Exception:
                return None
        else:
            return None
    else:
        return None
