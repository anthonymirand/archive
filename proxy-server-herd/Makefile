SHELL = /bin/bash

default: main.py
	@echo "No compilation required for Python script."
	@echo "To run proxy herd, use 'python main.py [server_name]'."
	@echo "NOTE: Run all servers in the foreground to prevent runaway servers."

run: main.py
	@printf "Enter a server name: "; \
	@read name || exit; \
	@echo -e "Starting...\n"; \
	python main.py $$name;

clean:
	@rm -r logs/
	@rm -r *.pyc
	@echo "Directory cleaned."
