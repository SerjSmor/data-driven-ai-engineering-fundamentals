# BuildGuild - AI Engineering Quests

A series of four interconnected AI engineering quests designed to teach prompt optimization, DSPy compilation, and LLM evaluation.

## Quests

1. **01-rag-evaluation** - RAG Baseline Evaluation
   - Measure retrieval performance for a help center RAG system
   - Build a baseline and produce evaluation metrics
   - *Based on [broken-help-center-quest](https://github.com/SerjSmor/broken-help-center-quest)*

2. **02-few-shot-prompt-optimization** - Few-Shot Prompt Optimization
   - Build a simple prompt optimizer from scratch
   - Learn data-driven prompt improvement principles

3. **03-atis-few-shot-dspy** - DSPy Few-Shot Optimization
   - Use DSPy framework for advanced prompt optimization
   - Compile and export optimized programs to production code

4. **04-llm-judge-calibration** - LLM as a Judge Calibration
   - Build and calibrate an LLM-based evaluation system
   - Incorporate semantic similarity and custom metrics

## Quick Start

```bash
# Install all modules
make install

# Install specific module
make install-01

# See all available commands
make help

# Run read-only workspace smoke checks
make check

# Verify the lockfile is current
make check-lock
```

## Structure

```
.
├── pyproject.toml          # Workspace config
├── uv.lock                 # Lockfile for reproducible builds
├── Makefile                # Quick commands
├── AGENTS.md               # General agent guidance
├── 01-rag-evaluation/
├── 02-few-shot-prompt-optimization/
├── 03-atis-few-shot-dspy/
└── 04-llm-judge-calibration/
```

## Development

This is a `uv` workspace. Each module is self-contained with its own `pyproject.toml` and `challenge.json`.

- **Builder role**: Implement quest tasks (see `AGENTS.md`)
- **Judge role**: Evaluate completed tasks (see `challenge.json`)

## Codex Quest Skill

This repository includes a local Codex plugin with the `$buildguild-start-quest` skill.
Install the repository marketplace, add the plugin, and start a new Codex thread before using it:

```bash
codex plugin marketplace add .
codex plugin add buildguild-start-quest@personal
```

Use `$buildguild-start-quest` or ask Codex to start a specific module. `/start-quest` is not a Codex command.

## Attribution

Quest 1 (RAG Evaluation) is based on [broken-help-center-quest](https://github.com/SerjSmor/broken-help-center-quest) by SerjSmor.
