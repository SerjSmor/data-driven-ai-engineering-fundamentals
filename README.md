# Data-Driven AI Engineering: Hands-On Quests

A free, hands-on roadmap for the fundamentals of **data-driven AI engineering**: evaluating LLM systems with real datasets and metrics, optimizing prompts with data, calibrating LLM judges, and building retrieval-augmented (RAG) chatbots.

Most AI engineering advice runs on vibes: tweak a prompt, eyeball a few outputs, ship. These quests take the other route. Every step starts from a dataset, a baseline, and a metric, so each change you make has numbers behind it.

## About the author

Hi, I'm **Serj Smor**. I wrote *Building LLM Applications with DSPy*, the first book on DSPy from a major publisher. I lead an Applied AI team at [Contentsquare](https://contentsquare.com), and I teach data science and AI engineering to hundreds of practitioners.

I built this repo because I kept seeing the same gap: engineers who could call an LLM API, but had no reliable way to tell whether their system was actually getting better. These quests are the fundamentals I wish everyone started with.

## Why these fundamentals

AI engineering fundamentals start with using an LLM to solve basic, everyday tasks well: **classification**, **summarization**, and **LLM-as-a-judge** evaluation, alongside a solid grasp of **retrieval-augmented generation (RAG)**. Almost every production LLM system is built from these blocks, and getting them right with data is what separates a demo from a product.

This repo turns each of those building blocks into a challenge with clear milestones, so you learn by building, measuring, and improving.

## What you'll build

The repo contains **four quests**. Each quest is a real project broken into **milestones**, and each milestone is a short list of concrete tasks. We recommend doing them in order, since later quests reuse ideas (and sometimes code) from earlier ones.

| # | Quest | What you build | Dataset |
|---|-------|----------------|---------|
| 1 | [Few-Shot Prompt Optimization](few-shot-prompt-optimization/) | A simple few-shot prompt optimizer for intent classification, written from scratch | [ATIS](https://huggingface.co/datasets/tuetschek/atis) |
| 2 | [ATIS Few-Shot Optimization with DSPy](atis-few-shot-dspy/) | The same classifier optimized with DSPy, then exported to plain OpenAI code for production | [ATIS](https://huggingface.co/datasets/tuetschek/atis) |
| 3 | [LLM Judge Calibration](llm-judge-calibration/) | A conversation summarizer and an LLM-as-a-judge calibrated against labelled examples | [DialogSum](https://huggingface.co/datasets/knkarthick/dialogsum) |
| 4 | [Knowledge Base Chatbot](knowledge-base-chatbot/) | A RAG chatbot with lexical search, grounded answers, and separate retrieval and answer evaluation | [WixQA](https://huggingface.co/datasets/Wix/WixQA) |

### Quest 1: Few-Shot Prompt Optimization
Build your own prompt optimizer before reaching for a framework.
1. **Quick EDA** – size, splits, labels, and message types in ATIS
2. **Calculate Baseline** – a zero-shot classifier, a metric, and a baseline score
3. **Create Naive Few-Shot Prompt Optimizer** – build prompts from random training examples
4. **Evaluate Naive Few-Shot Prompt** – compare against the baseline
5. **Create Multi-Seed Few-Shot Optimizer** – search over candidate prompts on a dev set
6. **Improve Optimizer Code Reuse** – refactor the optimizer into clean, reusable pieces

### Quest 2: ATIS Few-Shot Optimization with DSPy
Move from a hand-built optimizer to DSPy, then back to production code with no DSPy dependency.
1. **Create an ATIS Classification Service** – a single-message classifier interface
2. **DSPy Few-Shot Example** – reproducible splits, compile, inspect, evaluate honestly, track with MLflow
3. **DSPy Instruction-Based Example** – optimize instructions instead of examples
4. **Towards Production** – export the best program to native OpenAI code and verify at least 90% alignment

### Quest 3: LLM Judge Calibration for Conversation Summaries
Help a restaurant chain understand every customer conversation, and learn when you can trust an automated evaluator.
1. **EDA** – explore DialogSum and build small train/test samples
2. **Create the First Summarizer** – a baseline summarizer
3. **Test Familiar Evaluation Metrics** – ROUGE-style similarity and where it breaks
4. **Build an LLM Judge** – turn business rules into a rubric a judge can apply
5. **Calibrate the Judge** – good, bad, and ambiguous examples from the ground truth
6. **Use the Judge to Improve the Product** – find a weakness, fix it, report honestly
7. **Additional Metrics** – groundedness and completeness
8. **Summary**

### Quest 4: Knowledge Base Chatbot with WixQA
Build a chatbot that looks things up before it answers.
1. **Explore WixQA and the Knowledge Base** – profile the data, build a Streamlit explorer
2. **Build the Chatbot Mental Model** – draw the RAG flow and trace one example through it
3. **Build Lexical Search** – ranked retrieval with an interactive search UI
4. **Generate Answers from Retrieved Documents** – grounded prompts and a chatbot UI
5. **Evaluate Retrieval and Answers** – retrieval metrics plus end-to-end answer evaluation

## How it works

Each quest folder has the same layout:

```
<quest>/
├── README.md         # quest-specific instructions
├── challenge.json    # the quest definition: goal, dataset, milestones, tasks
├── progress.json     # your progress: task status and judge verdicts
├── app.py            # Streamlit workspace with hints, progress, and restart controls
├── scripts/          # mark_ready.py (and judge.py where available)
├── templates/        # starting shapes for the artifacts you'll create
└── user_artifacts/   # your work goes here (git-ignored, created as you go)
```

Tasks move through three states: **pending → ready_for_judgment → complete**. You (the builder) mark work ready. Only the judge marks it complete. A milestone is done when all its required tasks are complete. Bonus and optional tasks never block progress.

### Two ways to work (mix and match)

**1. Hands-on with the Streamlit apps.** Each quest has a Streamlit workspace (`app.py`) that shows the milestones, progressive hints, expected artifacts, and your progress. Open it, read the task, and write the code yourself.

**2. Guided by a coding agent.** Open the repo in a coding agent such as Claude Code, Codex, or Cursor and let it guide you through the instructions in each quest folder. [`AGENTS.md`](AGENTS.md) defines two roles:

- **Builder:** implements a pending task, saves artifacts under `user_artifacts/`, and marks it `ready_for_judgment`.
- **Judge:** reviews the work without fixing it, at the task's `judge_level` (`easy`, `medium`, or `hard`), and writes a verdict with evidence.

Keeping the roles separate means your work gets reviewed rather than graded by the same agent that wrote it.

You don't have to pick one. Many learners write the code themselves, track progress in Streamlit, and call in the agent as a judge or when they get stuck.

## Getting started

**Prerequisites:** Python 3.10+, git, and an API key for an LLM provider (most quests use OpenAI).

```bash
git clone https://github.com/SerjSmor/build-guild.git
cd build-guild/few-shot-prompt-optimization

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export OPENAI_API_KEY=sk-...   # or put it in a local .env file (git-ignored)
```

Open the Streamlit workspace to see milestones, hints, and your progress:

```bash
streamlit run app.py
# or, with uv:
uv run --with-requirements requirements.txt streamlit run app.py
```

Then work through the loop:

1. Read `challenge.json` (or the quest's README) and pick a pending task or milestone.
2. Build it, saving outputs to `user_artifacts/`. The `templates/` folder shows the expected shapes.
3. Mark it ready:
   ```bash
   python scripts/mark_ready.py --milestone eda --notes "Completed the EDA summary"
   ```
4. Get it judged, either by asking your coding agent to act as the Judge from `AGENTS.md` or by running `python scripts/judge.py` where the quest includes it.
5. Move to the next milestone. When a quest is done, start the next one.

Each quest's own README lists its exact milestone IDs and commands.

## Who this is for

- Software engineers moving into AI engineering
- Data scientists who want to ship LLM features with real evaluation behind them
- Anyone who has tuned a prompt by feel and wants a repeatable, measurable process

If these quests helped you, ⭐ star the repo and share it with someone learning AI engineering.

## Want the full course?

This repo is the free foundation. If you want a more streamlined, guided path with more depth, check out the full course at **[buildatadrivenai.com](https://www.buildatadrivenai.com)**.
