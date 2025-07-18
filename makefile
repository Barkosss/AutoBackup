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

# ...
client:
	@poetry run python3 -m src.KVStorage.client

# ...
server:
	@poetry run python3 -m src.KVStorage.server $(filter-out $@,$(MAKECMDGOALS))

# ...
console:
	@poetry run python3 -m src.KVStorage.console

# Run local tests
test:
	@poetry run python3 -m tests.test_start

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
