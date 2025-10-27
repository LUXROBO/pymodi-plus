.PHONY: help install install-dev install-editable reinstall test test-all test-input test-output test-task test-verbose lint format clean clean-build clean-pyc clean-test coverage docs dist release examples
.DEFAULT_GOAL := help

# Python interpreter detection
ifeq ($(shell which python3),)
	PYTHON = python
else
	PYTHON = python3
endif

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Check if command exists
define check_command
	@which $(1) > /dev/null 2>&1 || (echo "$(RED)Error: $(1) is not installed. Run 'make install-dev' first.$(NC)" && exit 1)
endef

##@ Help

help: ## Show this help message
	@echo "$(BLUE)PyMODI Plus - Makefile Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-18s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Setup

install: ## Install package dependencies
	@echo "$(BLUE)Installing package dependencies...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "$(GREEN)✓ Package dependencies installed successfully$(NC)"

install-dev: install ## Install package + development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(PYTHON) -m pip install pytest pytest-cov
	@echo "$(BLUE)Installing package in editable mode...$(NC)"
	$(PYTHON) -m pip install -e .
	@echo "$(GREEN)✓ Development dependencies installed successfully$(NC)"
	@echo "$(BLUE)Checking for dependency conflicts...$(NC)"
	@$(PYTHON) -m pip check && echo "$(GREEN)✓ No dependency conflicts found$(NC)" || echo "$(YELLOW)⚠ Some dependency warnings (may be safe to ignore)$(NC)"

install-editable: ## Install package in editable/development mode
	@echo "$(BLUE)Installing package in editable mode...$(NC)"
	$(PYTHON) -m pip install -e .
	@echo "$(GREEN)✓ Package installed in editable mode$(NC)"

reinstall: ## Reinstall package (fixes dependency issues)
	@echo "$(BLUE)Reinstalling package...$(NC)"
	$(PYTHON) -m pip uninstall -y pymodi-plus || true
	$(PYTHON) -m pip install -e .
	@echo "$(GREEN)✓ Package reinstalled$(NC)"

##@ Testing

test: ## Run all tests safely (avoiding pytest conflicts)
	$(call check_command,pytest)
	@echo "$(BLUE)Running tests...$(NC)"
	$(PYTHON) -m pytest tests/task/ tests/module/input_module/ tests/module/output_module/ -v
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-all: ## Run ALL tests including setup_module (may have conflicts)
	$(call check_command,pytest)
	@echo "$(BLUE)Running all tests (including potential conflicts)...$(NC)"
	$(PYTHON) -m pytest tests/ -v
	@echo "$(YELLOW)⚠ Some errors may occur due to pytest naming conflicts$(NC)"

test-input: ## Run input module tests only
	$(call check_command,pytest)
	@echo "$(BLUE)Running input module tests...$(NC)"
	$(PYTHON) -m pytest tests/module/input_module/ -v
	@echo "$(GREEN)✓ Input module tests completed$(NC)"

test-output: ## Run output module tests only
	$(call check_command,pytest)
	@echo "$(BLUE)Running output module tests...$(NC)"
	$(PYTHON) -m pytest tests/module/output_module/ -v
	@echo "$(GREEN)✓ Output module tests completed$(NC)"

test-task: ## Run task tests only
	$(call check_command,pytest)
	@echo "$(BLUE)Running task tests...$(NC)"
	$(PYTHON) -m pytest tests/task/ -v
	@echo "$(GREEN)✓ Task tests completed$(NC)"

test-verbose: ## Run tests with verbose output
	$(call check_command,pytest)
	@echo "$(BLUE)Running tests with verbose output...$(NC)"
	$(PYTHON) -m pytest tests/task/ tests/module/input_module/ tests/module/output_module/ -vv
	@echo "$(GREEN)✓ Tests completed$(NC)"

coverage: ## Run tests with coverage report
	$(call check_command,pytest)
	$(call check_command,coverage)
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	$(PYTHON) -m pytest tests/task/ tests/module/input_module/ tests/module/output_module/ --cov=modi_plus --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/index.html$(NC)"

##@ Code Quality

lint: ## Check code style with flake8
	$(call check_command,flake8)
	@echo "$(BLUE)Checking code style...$(NC)"
	flake8 modi_plus examples tests
	@echo "$(GREEN)✓ Code style check passed$(NC)"

format: ## Format code with black
	$(call check_command,black)
	@echo "$(BLUE)Formatting code...$(NC)"
	black modi_plus examples tests
	@echo "$(GREEN)✓ Code formatted successfully$(NC)"

##@ Examples

examples: ## List all available examples
	@echo "$(BLUE)Available Examples:$(NC)"
	@echo ""
	@echo "$(YELLOW)Basic Usage Examples:$(NC)"
	@ls -1 examples/basic_usage_examples/*.py | xargs -n1 basename | sed 's/^/  - /'
	@echo ""
	@echo "$(YELLOW)Creation Examples:$(NC)"
	@ls -1 examples/creation_examples/*.py 2>/dev/null | xargs -n1 basename | sed 's/^/  - /' || echo "  (no examples found)"
	@echo ""
	@echo "$(YELLOW)Intermediate Examples:$(NC)"
	@ls -1 examples/intermediate_usage_examples/*.py 2>/dev/null | xargs -n1 basename | sed 's/^/  - /' || echo "  (no examples found)"
	@echo ""
	@echo "Run an example with: $(GREEN)python examples/basic_usage_examples/<example_name>.py$(NC)"

##@ Cleanup

clean: clean-build clean-pyc clean-test ## Remove all build, test, coverage and Python artifacts

clean-build: ## Remove build artifacts
	@echo "$(BLUE)Removing build artifacts...$(NC)"
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	@echo "$(GREEN)✓ Build artifacts removed$(NC)"

clean-pyc: ## Remove Python file artifacts
	@echo "$(BLUE)Removing Python file artifacts...$(NC)"
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	@echo "$(GREEN)✓ Python file artifacts removed$(NC)"

clean-test: ## Remove test and coverage artifacts
	@echo "$(BLUE)Removing test and coverage artifacts...$(NC)"
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	@echo "$(GREEN)✓ Test artifacts removed$(NC)"

##@ Documentation

docs: ## Generate Sphinx HTML documentation
	$(call check_command,sphinx-apidoc)
	@echo "$(BLUE)Generating documentation...$(NC)"
	rm -f docs/modi_plus.*
	rm -f docs/modules.md
	sphinx-apidoc -o docs/ modi_plus
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@echo "$(GREEN)✓ Documentation generated in docs/_build/html/index.html$(NC)"

##@ Build & Release

dist: clean ## Build source and wheel package
	@echo "$(BLUE)Building distribution packages...$(NC)"
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build
	ls -l dist
	@echo "$(GREEN)✓ Distribution packages built$(NC)"

release: dist ## Package and upload a release
	$(call check_command,twine)
	@echo "$(BLUE)Uploading to PyPI...$(NC)"
	twine upload dist/*
	@echo "$(GREEN)✓ Release uploaded$(NC)"
