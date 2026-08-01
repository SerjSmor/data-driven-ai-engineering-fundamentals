.PHONY: help install install-all install-01 install-02 install-03 install-04 check check-lock stop-quests clean

help:
	@echo "BuildGuild - uv workspace with modular quests"
	@echo ""
	@echo "Installation:"
	@echo "  make install-all    - Install all module dependencies"
	@echo "  make install-01     - Install 01-rag-evaluation dependencies"
	@echo "  make install-02     - Install 02-few-shot-prompt-optimization dependencies"
	@echo "  make install-03     - Install 03-atis-few-shot-dspy dependencies"
	@echo "  make install-04     - Install 04-llm-judge-calibration dependencies"
	@echo ""
	@echo "Verification:"
	@echo "  make check          - Run read-only workspace smoke checks"
	@echo "  make check-lock     - Verify uv.lock is current"
	@echo "  make stop-quests    - Stop local Streamlit quests on ports 8502-8504"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove .venv and uv.lock"

install-all: venv install-01 install-02 install-03 install-04
	@echo "✓ All modules installed"

install: install-all

venv:
	@if [ ! -d ".venv" ]; then uv venv; fi

install-01:
	@echo "Installing 01-rag-evaluation dependencies..."
	uv pip install -r 01-rag-evaluation/requirements.txt

install-02:
	@echo "Installing 02-few-shot-prompt-optimization dependencies..."
	uv pip install -r 02-few-shot-prompt-optimization/requirements.txt

install-03:
	@echo "Installing 03-atis-few-shot-dspy dependencies..."
	uv pip install -r 03-atis-few-shot-dspy/requirements.txt

install-04:
	@echo "Installing 04-llm-judge-calibration dependencies..."
	uv pip install -r 04-llm-judge-calibration/requirements.txt

check:
	python3 scripts/check_workspace.py

check-lock:
	uv lock --check

stop-quests:
	@for port in 8502 8503 8504; do \
		pids="$$(lsof -tiTCP:$$port -sTCP:LISTEN || true)"; \
		if [ -n "$$pids" ]; then \
			echo "Stopping quest on port $$port (PID $$pids)..."; \
			kill $$pids; \
		fi; \
	done

clean:
	rm -rf .venv uv.lock
	@echo "✓ Cleaned .venv and uv.lock"

.DEFAULT_GOAL := help
