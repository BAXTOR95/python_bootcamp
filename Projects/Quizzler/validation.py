import logging

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


def validate_trivia_parameters(questions, category, difficulty):
    if not isinstance(questions, int) or questions < 0:
        logging.error("Invalid number of questions.")
        return False
    if not isinstance(category, int) or category < 0:
        logging.error("Invalid category.")
        return False
    if difficulty not in ["easy", "medium", "hard"]:
        logging.error("Invalid difficulty level.")
        return False
    return True
