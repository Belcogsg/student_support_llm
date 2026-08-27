import json
from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).parent.parent
PDF_FILE = BASE_DIR / "docs" / "UDSM_Almanac_2025_26.pdf"
ARIS_FILE = Path(__file__).parent / "docs" / "aris_guide.json"

if not PDF_FILE.exists():
    PDF_FILE = BASE_DIR / "docs" / "UDSM_Almanac_2025_26"


def get_aris_context(question: str) -> str:
    """Reads structured ARIS portal guidance if the question asks about portal processes."""
    if not ARIS_FILE.exists():
        return ""
    
    with open(ARIS_FILE, "r", encoding="utf-8") as f:
        aris_data = json.load(f)
        
    q_lower = question.lower()
    
    if any(k in q_lower for k in ["register", "course", "aris", "portal", "add class"]):
        reg = aris_data.get("course_registration", {})
        steps = "\n".join(reg.get("steps", []))
        
        return f"[ARIS 3.0 Guide]\nSystem: {reg.get('system')}\nURL: {reg.get('portal_url')}\nPrerequisites: {reg.get('prerequisites')}\nSteps:\n{steps}"
        
    return ""


def retrieve_context(question: str) -> str:
    """Combines ARIS system guide with Almanac PDF search."""
    context_blocks = []
    
    # checking aris guide
    aris_info = get_aris_context(question)
    
    if aris_info:
        context_blocks.append(aris_info)
        
    # Checking almanac
    if PDF_FILE.exists():
        reader = PdfReader(PDF_FILE)
        ignore_words = {"when", "does", "the", "is", "a", "an", "of", "in", "to", "for", "what", "on", "how"}
        keywords = [w.lower() for w in question.split() if w.lower() not in ignore_words]
        
        matched_pages = []
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            text_lower = text.lower()
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > 0:
                matched_pages.append((matches, page_idx + 1, text))
                
        matched_pages.sort(key=lambda x: x[0], reverse=True)
        top_matches = matched_pages[:2]
        
        for score, page_num, text in top_matches:
            context_blocks.append(f"[Almanac Page {page_num}]\n{text.strip()}")
        
    if not PDF_FILE.exists():
        print(f"[ERROR] PDF file not found at: {PDF_FILE.resolve()}")
        return ""
    
    if not context_blocks:
        return "No specific UDSM guides or almanac pages found."
        
    return "\n\n---\n\n".join(context_blocks)