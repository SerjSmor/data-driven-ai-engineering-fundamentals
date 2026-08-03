# Knowledge Base Chatbot with WixQA

Build a small retrieval-augmented chatbot for Wix support questions. The quest moves from dataset exploration to a lexical search baseline, grounded LLM answers, and separate retrieval and answer evaluation.

Learner-created work belongs in `user_artifacts/`. Starting shapes belong in `templates/`.

## Dataset

Use [Wix/WixQA](https://huggingface.co/datasets/Wix/WixQA):

```python
from datasets import load_dataset

qa = load_dataset("Wix/WixQA", "wixqa_expertwritten", split="train")
kb = load_dataset("Wix/WixQA", "wix_kb_corpus", split="train")
```

The QA rows contain `question`, `answer`, and `article_ids`. Corpus rows contain `id`, `url`, `contents`, and `article_type`. An `article_ids` value points to the corpus documents that support an answer.

## Builder flow

1. Read `challenge.json` and pick one pending task.
2. Build the expected artifact under `user_artifacts/`.
3. Mark it ready without marking it complete:

```bash
python scripts/mark_ready.py profile_dataset --notes "Profiled both WixQA configurations"
python scripts/mark_ready.py --milestone lexical_retrieval --notes "Implemented and tested lexical search"
```

Suggested milestone commands:

```bash
python scripts/mark_ready.py --milestone explore_wixqa
python scripts/mark_ready.py --milestone chatbot_mental_model
python scripts/mark_ready.py --milestone lexical_retrieval
python scripts/mark_ready.py --milestone grounded_answers
python scripts/mark_ready.py --milestone evaluation
```

## Judge flow

Only judge work already marked `ready_for_judgment`:

```bash
python scripts/judge.py
python scripts/judge.py --task implement_retriever
```

The judge performs artifact, structure, and Python syntax checks. Hard tasks receive additional implementation-signal checks. Live provider calls are not required for static judging.

## Quest UI

```bash
streamlit run app.py
```

The learner-built explorers and chatbot are separate expected artifacts under `user_artifacts/`.
