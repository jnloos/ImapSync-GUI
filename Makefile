APP_NAME := ImapSync-GUI
SRC := main.py
BIN_DIR := bin

.PHONY: all clean linux windows

all: linux windows

linux:
	pyinstaller \
	  --onefile \
	  --windowed \
	  --add-data "locales:locales" \
	  --name $(APP_NAME) \
	  --distpath $(BIN_DIR) \
	  $(SRC)
	@echo "Created $(BIN_DIR)/$(APP_NAME)"

windows:
	pyinstaller \
	  --onefile \
	  --windowed \
	  --add-data "locales:locales" \
	  --name $(APP_NAME).exe \
	  --distpath $(BIN_DIR) \
	  $(SRC)
	@echo "Created $(BIN_DIR)/$(APP_NAME).exe"

clean:
	rm -rf build dist __pycache__ *.spec