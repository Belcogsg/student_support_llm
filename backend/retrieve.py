from pathlib import Path

FAQ_FILE = Path(__file__).parent /"data"/"university_faq.txt"

with open(FAQ_FILE, encoding="utf-8") as f:
    FAQ_TEXT = f.read()
    

def retrieve_context(question):
    question = question.lower()
    sections = FAQ_TEXT.split("\n\n")
    matches = []

    for section in sections:
        if any(word in section.lower() for word in question.split()):
            matches.append(section)

    if matches:
        return "\n\n".join(matches)

    return "No relevant university information found."