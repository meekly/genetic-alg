PYTHON    := python3
DATA_FILE := 4.txt
OUT_FILE  := 4.json

define remove
	find . -name $(1) -exec rm -rf \{\} \; ||:
endef

# Starting learning algorithm
learn:
	$(PYTHON) process.py $(DATA_FILE) | tee $(OUT_FILE)

# Removing all temporary files
clean:
	@$(call remove, '__pycache__')
	@$(call remove, '*.pyc')
	@$(call remove, '#*')
	@$(call remove, '*~')
	@$(call remove, '.#*')
	@$(call remove, '$(OUT_FILE)')
