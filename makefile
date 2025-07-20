.PHONY: venv install format lint

# Information about venv
venv:
	@python3 -m venv venv
	@echo "Activate venv:"
	@echo "Linux/macOS: source venv/bin/activate"
	@echo "Windows: .\\\\venv\\\\Scripts\\\\activate"

# Install all dependencies
install: venv
	@poetry install

telegram:
	@python3 src/telegrambot/main.py

# Run local tests
test:
	@echo "Is not supported"

# Check project files with formatter and linter
check: format lint

# Formatter Commands
format:
	@poetry run isort .
	@poetry run black .

# Linter Commands
lint:
	@poetry run flake8 src/
	@poetry run mypy src/
