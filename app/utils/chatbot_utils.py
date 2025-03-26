QUESTION_SUGGESTIONS = {
    "employee": [
        "How many employees are there?",
        "What are the names of all employees?",
        "Who are the employees in the sales department?",
        "What is the salary of a particular employee?",
    ],
    "client": [
        "How many clients do we have?",
        "What are the names of all clients?",
        "Which clients have ongoing projects?",
        "What is the budget of a particular client?",
    ],
    "sale": [
        "What is the total sale till today?",
        "How much budget do we have from all clients?",
    ]
}

def get_suggestions(user_input: str):
    """Returns question suggestions based on keywords in user input."""
    suggestions = []
    
    for keyword, questions in QUESTION_SUGGESTIONS.items():
        if keyword in user_input.lower():
            suggestions.extend(questions)
    
    return suggestions if suggestions else ["I couldn't find related questions. Try a different query."]
