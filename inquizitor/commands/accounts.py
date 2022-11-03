import click
import csv
import logging
import secrets
import os
from sqlmodel import Session, create_engine
from typing import Optional
import unidecode

from inquizitor import crud, models
from inquizitor.commands.initial_data import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('email')
@click.argument('last_name')
@click.argument('first_name')
@click.option('--username', default=None, type=str)
@click.option('--password', default=None, type=str)
@click.option('--is-student', default=False, type=bool)
@click.option('--is-teacher', default=False, type=bool)
@click.option('--is-admin', default=False, type=bool)
@click.option('--is-cheater-dataset', default=False, type=bool)
def create_account(
    email: str, last_name: str, first_name: str,
    username: str, password: str,
    is_student: bool, is_teacher: bool, is_admin: bool,
    is_cheater_dataset: bool
) -> None:
    """
        Create a student account with the provided details, 
        and then send an email containing login credentials
        to get app access.
    """
    last_name = last_name.capitalize()
    first_name = first_name.capitalize()
    username = username or f'{last_name}{"".join(first_name.split(" "))}'.lower()
    user_in = models.UserCreate(
        username=username,
        email=email,
        full_name=f'{last_name}, {first_name}',
        last_name=last_name,
        first_name=first_name,
        is_student=is_student,
        is_teacher=is_teacher,
        is_admin=is_admin,
        password=password or secrets.token_hex(4),
        is_cheater_dataset=is_cheater_dataset
    )
    try:
        user = crud.user.create(db, obj_in=user_in)
        logger.info(f"Account {username} successfully created!")
    except Exception as e:
        logger.info(f"Error: {e.value}")
        logger.info(f"Account with email {email} or username {username} already exists!")

@click.command()
@click.argument('filepath')
@click.argument('heroku_app', required=False)
@click.option(
    '--is-cheater-dataset', 
    prompt='Is this group to be included in the cheaters dataset?',
    default=False,
    type=bool
)
def create_accounts(
    filepath: str, 
    is_cheater_dataset: bool,
    heroku_app: Optional[str] = None,
):
    """
        Create accounts from a csv file.
    """
    if not filepath.endswith('.csv'):
        logger.info('File should be in CSV')
        return

    base_command = f'heroku run python main.py create-account %s --app {heroku_app}'
    if not heroku_app:
        base_command = 'python main.py create-account %s'
        
    total_accounts = 0
    with open(filepath, newline='') as csvf:
        account_reader = csv.reader(csvf)
        output_file = open(f'{filepath.split(os.sep)[-1].split(".")[0]}-password.csv', 'w', newline='')
        output_writer = csv.writer(output_file)
        output_writer.writerow(['email', 'username', 'password'])
        email_index, fullname_index = None, None
        logger.info('Creating accounts...')
        for i, row in enumerate(account_reader):
            if i == 0:
                try:
                    email_index = row.index('Email Address')
                    fullname_index = row.index('Full Name')
                except:
                    logger.info('File does not contain required headers: "Email Address" and "Full Name"')
                    return
            else:
                password = secrets.token_hex(4)
                last_name, first_name = row[fullname_index].split(',')
                res = os.system(
                    base_command % f'{row[email_index]} "{last_name}" "{first_name.strip()}" --password={password} --is-student=True --is-cheater-dataset={is_cheater_dataset}'
                )
                if res == 0:
                    username = f'{last_name}{"".join(first_name.split(" "))}'.lower()
                    output_writer.writerow([row[email_index], username, password])
                total_accounts += 1 if res == 0 else 0 # 0 = success; 1 or 2 = failure
        output_file.close()

    logger.info(f'Successfully created {total_accounts} accounts!')

@click.command()
@click.argument('filepath')
@click.argument('database_url')
@click.option(
    '--is-cheater-dataset', 
    prompt='Is this group to be included in the cheaters dataset?',
    default=False,
    type=bool
)
@click.option(
    '--is-teacher', 
    prompt='Is this group for teachers?',
    default=False,
    type=bool
)
@click.option(
    '--teachers-have-dummy-quizzes', 
    prompt='Add dummy quizzes? (This option is strictly for testing only)',
    default=False,
    type=bool
)
@click.option(
    '--password', 
    prompt='Password [Leave blank to randomize]',
    default=secrets.token_hex(4),
    type=str
)
def create_accounts_on_db(
    filepath: str, 
    is_cheater_dataset: bool,
    is_teacher: bool,
    database_url: str,
    teachers_have_dummy_quizzes: bool,
    password: str
):
    """
        Create accounts from a csv file on target deployed database.
    """
    if not filepath.endswith('.csv'):
        logger.info('File should be in CSV')
        return

    engine = create_engine(database_url)
    total_accounts = 0
    with open(filepath, newline='') as csvf:
        account_reader = csv.reader(csvf)
        output_file = open(f'{filepath.split(os.sep)[-1].split(".")[0]}-password.csv', 'w', newline='')
        output_writer = csv.writer(output_file)
        output_writer.writerow(['email', 'username', 'password'])
        email_index, fullname_index = None, None
        logger.info('Creating accounts...')
        for i, row in enumerate(account_reader):
            if i == 0:
                try:
                    email_index = row.index('Email Address')
                    fullname_index = row.index('Full Name')
                except:
                    logger.info('File does not contain required headers: "Email Address" and "Full Name"')
                    return
            else:
                email=row[email_index]
                password=password
                last_name, first_name = row[fullname_index].split(',')
                last_name = unidecode.unidecode(last_name).capitalize().strip().replace("a+-", "n") # replace enye
                first_name = unidecode.unidecode(first_name).capitalize().strip().replace("a+-", "n")
                username = f'{"".join(last_name.split(" "))}{"".join(first_name.split(" "))}'.lower().replace(".", "") # remove middle initial dot
                user_in = models.UserCreate(
                    username=username,
                    email=email,
                    full_name=f'{last_name}, {first_name}',
                    last_name=last_name,
                    first_name=first_name,
                    is_student=not is_teacher,
                    is_teacher=is_teacher,
                    is_admin=False,
                    password=password,
                    is_cheater_dataset=is_cheater_dataset
                )
                with Session(engine) as session:
                    try:
                        user = crud.user.create(session, obj_in=user_in)
                        output_writer.writerow([email, username, password])
                        logger.info(f"Account {username} successfully created!")
                        total_accounts += 1

                        if is_teacher and teachers_have_dummy_quizzes:
                            quizzes = crud.quiz.get_multi(session)
                            quiz = crud.quiz.get(session, id=user.id)
                            quiz_in = models.QuizUpdate(teacher_id=user.id)
                            quiz = crud.quiz.update(session, db_obj=quiz, obj_in=quiz_in)
                    except Exception as e:
                        # logger.info(f"Error: {e}")
                        logger.info(f"Account with email {email} or username {username} already exists!")
        output_file.close()

    logger.info(f'Successfully created {total_accounts} accounts!')
                
@click.command()
@click.argument('email')
@click.argument('password', required=False)
def reset_password(email: str, password: str = None) -> None:
    """
        Reset password to a randomly generated code if password is not supplied.
    """
    user = crud.user.get_by_email(db, email=email)
    user_in = models.UserUpdate(password=password or secrets.token_hex(4))

    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    if user:
        logger.info(f"Password of account {email} has been updated!")
    else:
        logger.info(f"Password reset failed.")