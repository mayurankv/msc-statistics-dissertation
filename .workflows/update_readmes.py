# Imports
import re
from re import Match


# Functions
def read_stub_file(
	match: Match[str],
) -> str:
	"""
	read_stub_file Read stub file and extract contents

	Args:
		match (Match[str]): Regex match object

	Returns:
		str: File content
	"""
	stub = match.group(1)
	with open(file=stub, mode="r") as file:
		file_content = file.read()
	return file_content


# Main function
def main() -> None:
	"""
	main Updating README.md
	"""
	with open(file="README.stub", mode="r") as file:
		readme_stub = file.read()

	# Replace stubs with file contents
	readme = re.sub(
		pattern=r"\{\{([^}]*)\}\}",
		repl=read_stub_file,
		string=readme_stub,
	).strip()

	# Update README.md
	with open(file="README.md", mode="w") as file:
		file.write(readme)


if __name__ == "__main__":
	main()
