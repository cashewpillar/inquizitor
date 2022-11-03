import click

from .initial_data import initial_data, add_exam
from .accounts import create_account, create_accounts, create_accounts_on_db, reset_password
from .attempts import invalidate_attempt

@click.group()
def cli():
    pass
