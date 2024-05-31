# Imports
from typer import Typer

# Initialise Decorators
app = Typer()


# Main Function
@app.command()
def main():
	pass


# Guarded Script
if __name__ == "__main__":
	app()
