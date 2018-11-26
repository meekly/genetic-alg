PYTHON    := python3
DATA_FILE := 4.txt
OUT_FILE  := 4.json

define remove
	find . -name $(1) -exec rm -rf \{\} \; ||:
endef

# Starting learning algorithm
bag:
	$(PYTHON) process.py $(DATA_FILE) 2>/dev/null | tee $(OUT_FILE)

# Removing all temporary files
clean:
	@$(call remove, '__pycache__')
	@$(call remove, '*.pyc')
	@$(call remove, '#*')
	@$(call remove, '*~')
	@$(call remove, '.#*')
	@$(call remove, '$(OUT_FILE)')
