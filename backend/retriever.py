from pathlib import Path

FAQ_FILE = Path(__file__).parent / "university_faq.txt"

def retrieve_context(question):
    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        knowledge = file.readlines()

    question_words = set(question.lower().split())

    best_line = ""
    best_score = 0

    for line in knowledge:
        score = 0

        for word in question_words:
            if word in line.lower():
                score += 1

        if score > best_score:
            best_score = score
            best_line = line.strip()

    return best_line