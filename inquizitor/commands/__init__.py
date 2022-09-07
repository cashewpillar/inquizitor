import click

from .initial_data import initial_data, add_exam
from .accounts import create_account, create_accounts


@click.group()
def cli():
    pass
