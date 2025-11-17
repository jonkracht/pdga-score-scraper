#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = pdga-score-scraper
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	@bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_VERSION); else mkvirtualenv.bat $(PROJECT_NAME) --python=$(PYTHON_VERSION); fi"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
	




## Install Python dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -e .
	

.PHONY: update_requirements
update_requirements:
	pip list --format=freeze --exclude-editable > requirements.txt

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using flake8, black, and isort (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 pdga_score_scraper
	isort --check --diff pdga_score_scraper
	black --check pdga_score_scraper

## Format source code with black
.PHONY: format
format:
	isort pdga_score_scraper
	black pdga_score_scraper





#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make dataset
.PHONY: data
data: requirements
	#TODO:  Check if datasets already exists before re-downloading it; newline character not rendered correctly
	@read -p  "\nEnter event identification number:  " event_id; \
	$(PYTHON_INTERPRETER) pdga_score_scraper/dataset.py $$event_id && $(PYTHON_INTERPRETER) pdga_score_scraper/features.py $$event_id


## Create report
.PHONY: make_report
make_report:
	@read -p  "\nEnter event identification number:  " event_id 

	# Name of notebook WITHOUT .ipynb extension
	notebookName="4.01-jk-eda-report"
	
	# Run notebook
	jupyter-nbconvert --to notebook --execute --inplace "notebooks/4.01-jk-eda-report.ipynb" --Execute.Preprocessor.kernel_name=pdga_score_scraper

	#currentDate=`date +"%Y-%m-%d"`

	#pdfName="$(event_id)-report-$(currentDate).pdf"
	pdfName="test.pdf"

	# Convert to pdf
	#jupyter-nbconvert $$notebookName --to pdf --output "reports/$pdfName"
	jupyter-nbconvert "notebooks/4.01-jk-eda-report.ipynb" --to pdf --output-dir="reports" --output "test.pdf"


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

# Prints line above target when `make help` is executed
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
