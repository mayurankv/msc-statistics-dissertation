# Imports
from typer import Typer

# Initialise Classes
app = Typer()


@app.command()
def main():
	pass


# Guarded Script
if __name__ == "__main__":
	app()
