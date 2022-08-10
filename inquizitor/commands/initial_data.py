import click
import logging

from inquizitor.db.session import engine, SessionLocal
from inquizitor.db.init_db import init_db, drop_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init(use_realistic_data: bool = False) -> None:
    db = SessionLocal()
    init_db(db, engine, use_realistic_data=use_realistic_data)

@click.command()
@click.option(
    '--use-realistic-data', 
    prompt='Would you like to use realistic quiz data? \n(Requires internet connection to access Open Trivia DB)',
    default=True,
    type=bool
)
def initial_data(use_realistic_data: bool) -> None:
    print()
    logger.info("Dropping tables")
    drop_db(engine)

    logger.info("Creating initial data")
    init(use_realistic_data=use_realistic_data)
    logger.info("Initial data created")

@click.command()
def test():
    click.echo("hello world!")
