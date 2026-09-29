# OpenMP LLM Concurrency Verification Benchmark

This repository evaluates the capability of modern Large Language Models (LLMs) to verify the functional correctness and concurrency safety of OpenMP C code.

## Benchmark Overview
- **Dataset**: 7 OpenMP C programs covering standard parallel constructs (`critical`, `barrier`, `drb`, `flush`, `firstprivate`, `single nowait`, `task depend`).
- **Prompt Strategies**:
  - `naive.txt`: Direct code verification without prior domain examples.
  - `few_shot.txt`: In-context examples demonstrating step-by-step reasoning on parallel race conditions.
- **Evaluated Models**: `gpt-3.5-turbo`, `gpt-4o-mini`, `gpt-4o`, `gpt-5.4`, and `groq/qwen/qwen3.8-27b`.

## Repository Structure
.
├── openmp/             # C code benchmark implementations & specification JSON
├── prompts/            # Prompt templates (naive.txt, few_shot.txt)
├── results/            # Saved raw text outputs per model execution
├── results.csv         # Aggregated benchmark evaluation logs
├── run_eval.py         # LiteLLM test runner
├── FINDINGS.md         # In-depth benchmark conclusions and bug analysis
└── README.md


## Running the Evaluation
To execute the benchmark against any supported model:

```bash
python run_eval.py --model gpt-4o --prompt-file naive.txt --code-file barrier_correct.c

---

### Step 3: Proposed `FINDINGS.md`

Create `FINDINGS.md` to document key takeaways from your evaluation data:

```markdown
# OpenMP LLM Evaluation Findings & Analysis

## Key Takeaways

1. **`gpt-5.4` and `gpt-4o` Standardize Top Performance**
   - Both models performed reliably on standard code patterns, scoring 85.7% accuracy under `naive.txt`.
   - `firstprivate_initialization.c` posed a challenge across multiple frontier models, as models frequently misinterpret scoping rules for private variable copies.

2. **Negative Delta in Few-Shot Prompting for Mid-Sized Models**
   - Counterintuitively, `few_shot.txt` degraded accuracy for smaller models (`gpt-3.5-turbo` dropped from 85.7% to 57.1%). 
   - Long reasoning demonstrations caused smaller models to overfit to negative examples, leading them to falsely flag safe constructs (e.g., `barrier_correct.c` and `task_depend_sync.c`) as `INCORRECT`.

3. **Rate Limits & Unparsed Output (`groq/qwen/qwen3.8-27b`)**
   - On `few_shot.txt`, Qwen experienced high output token counts that hit API rate limits or generated extended reasoning blocks, resulting in `UNKNOWN` verdict extractions.
   - Restricting max output tokens or enforcing fixed string formats (`VERDICT: CORRECT`) is necessary when benchmarking models on rate-limited tiers.

## Accuracy Summary Table

| Model | Naive Pass Rate | Few-Shot Pass Rate | Overall Accuracy |
| :--- | :---: | :---: | :---: |
| **gpt-5.4** | **85.7%** | **85.7%** | **85.7%** |
| **gpt-4o** | **85.7%** | **85.7%** | **85.7%** |
| **gpt-3.5-turbo** | 85.7% | 57.1% | 71.4% |
| **gpt-4o-mini** | 85.7% | 57.1% | 71.4% |
| **groq/qwen/qwen3.8-27b** | 71.4% | 28.6% | 50.0% |