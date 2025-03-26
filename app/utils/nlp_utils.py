import spacy

nlp = spacy.load("en_core_web_sm")  # Load NLP model

def extract_name(doc):
    """Extracts a person's name from the query."""
    for ent in doc.ents:
        if ent.label_ == "PERSON":  # Detect names
            return ent.text
    return None

def extract_department(doc):
    """Extracts department from the query."""
    departments = ["HR", "Engineering", "Marketing", "Finance"]  # Add more if needed
    for token in doc:
        if token.text.capitalize() in departments:
            return token.text.capitalize()
    return None

def extract_role(doc):
    """Extracts job roles from the query."""
    roles = ["Manager", "Developer", "Engineer", "Analyst", "Designer"]  # Add more if needed
    for token in doc:
        if token.text.capitalize() in roles:
            return token.text.capitalize()
    return None

def process_query(query: str):
    """Processes the user query and returns an NLP-parsed document."""
    return nlp(query.lower())