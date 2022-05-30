from inquizitor import create_app
from inquizitor.commands import cli

app = create_app()

if __name__ == "__main__":
	cli()