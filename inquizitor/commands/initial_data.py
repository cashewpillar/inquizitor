import click
import logging
import re
import pprint

from inquizitor.db.session import engine, SessionLocal
from inquizitor.db.init_db import init_db, drop_db, add_quiz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
db = SessionLocal()

def init(use_realistic_data: bool = False) -> None:
    init_db(db, engine, use_realistic_data=use_realistic_data)

@click.command()
@click.option(
    '--use-realistic-data', 
    prompt='Would you like to use realistic quiz data? \n(Requires internet connection to access Open Trivia DB)',
    default=True,
    type=bool
)
def initial_data(use_realistic_data: bool) -> None:
    """
        Create initial data for the Quiz API.
        WARNING: This deletes existing data and should ideally be ran only once, during initial launch of the API.
    """
    print()
    logger.info("Dropping tables")
    drop_db(engine)

    logger.info("Creating initial data")
    init(use_realistic_data=use_realistic_data)
    logger.info("Initial data created")

@click.command()
@click.option(
    '--generate-attempts', 
    prompt='Would you like your quiz to initially have randomly generated attempts?',
    default=False,
    type=bool
)
@click.argument('filename')
def add_exam(filename: str, generate_attempts: bool):
    """
        Reads the data folder for default exams and adds them to the database 
    """
    # NOTE: another regex can be built to validate input to follow the same structure as the sample mock exam txt
    # NOTE: might best be placed on a utils module within project
    # NOTE: consider using yaml instead of txt
    QUIZ_NAME_REGEX = re.compile(r'(Name:) ?(.+)')
    QUIZ_DESC_REGEX = re.compile(r'(Desc:) ?(.+)')
    QUESTION_REGEX = re.compile(r'(\d+\.) ?(.*)')
    BLANKS_ANSWER_REGEX = re.compile(r'(Answer:) ?(.+)')
    CHOICES_CORRECT_ANSWER_REGEX = re.compile(r'(Correct Answer:) ?(.+)')
    json_data = {"items": []}
    if filename.endswith('.txt'):
        with open(f"inquizitor/data/{filename}", 'r') as f:
            text_data = f.readlines()
            logger.info("Adding quiz items...")
            for line in text_data:
                question_match = QUESTION_REGEX.search(line)
                blanks_answer_match = BLANKS_ANSWER_REGEX.search(line)
                choices_answer_match = re.split(r'\b[a-dA-D]\. ', line)[1:]
                choices_correct_answer_match = CHOICES_CORRECT_ANSWER_REGEX.search(line)
                quiz_name_match = QUIZ_NAME_REGEX.search(line)
                quiz_desc_match = QUIZ_DESC_REGEX.search(line)

                if quiz_name_match:
                    json_data['name'] = quiz_name_match.group(2).strip()
                elif quiz_desc_match:
                    json_data['desc'] = quiz_desc_match.group(2).strip()
                elif question_match:
                    json_data['items'].append({"question": question_match.group(2).strip()})
                elif choices_answer_match:
                    json_data['items'][-1]["incorrect_answers"] = [c.strip() for c in choices_answer_match]
                    json_data['items'][-1]["question_type"] = "multiple-choice"
                elif choices_correct_answer_match:
                    json_data['items'][-1]["correct_answer"] = choices_correct_answer_match.group(2).strip()
                elif blanks_answer_match:
                    json_data['items'][-1]["correct_answer"] = blanks_answer_match.group(2).strip()
                    json_data['items'][-1]["question_type"] = "fill-in-the-blank"
    
        add_quiz(db, json_data)
        logger.info("Quiz added successfully!")