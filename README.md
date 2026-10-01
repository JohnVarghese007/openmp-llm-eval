# OpenMP LLM Concurrency Verification Benchmark

This repository evaluates the capability of modern Large Language Models (LLMs) to verify the functional correctness and concurrency safety of OpenMP C code.

## Benchmark Overview
- **Dataset**: 8 OpenMP C programs covering standard parallel constructs (`critical`, `barrier`, `flush`, `firstprivate`, `single nowait`, `task depend`, `collapse`).
- **Prompt Strategies**:
  - `naive.txt`: Direct code verification without prior domain examples.
  - `few_shot.txt`: In-context examples demonstrating step-by-step reasoning on parallel race conditions.
- **Evaluated Models**: `gpt-3.5-turbo`, `gpt-4o-mini`, `gpt-4o`, `gpt-5.4`, and `groq/qwen/qwen3.8-27b`.

---

## Dataset Breakdown & Verification Objectives (8 Snippets)

This benchmark evaluates OpenMP code verification across 8 distinct parallel programming paradigms:

| Benchmark File | OpenMP Feature / Pattern | Concurrency Pattern & Objective | Ground Truth |
| :--- | :--- | :--- | :---: |
| `critical_section.c` | Mutual Exclusion (`#pragma omp critical`) | Verifies thread-safe updates to shared variables under mutual exclusion locks. | **CORRECT** |
| `barrier_correct.c` | Explicit Barriers (`#pragma omp barrier`) | Evaluates reasoning on `happens-before` execution ordering across concurrent thread execution. | **CORRECT** |
| `drb_example.c` | Unsynchronized Shared Access | Tests detection of data races caused by unsynchronized array writes in parallel loops. | **INCORRECT** |
| `flush_barrier_sync.c` | Memory Visibility (`#pragma omp flush`) | Tests recognition of explicit memory flushes and variable cache synchronization across threads. | **INCORRECT** |
| `firstprivate_initialization.c` | Variable Scoping (`firstprivate`) | Verifies if models correctly distinguish between thread-private variables and global scope updates. | **INCORRECT** |
| `single_nowait_barrier.c` | Task Synchronization (`single nowait`) | Evaluates detection of race conditions resulting from omitting implicit barriers on single-threaded regions. | **INCORRECT** |
| `task_depend_sync.c` | Task Graphs (`depend(in/out)`) | Tests verification of explicit task-dependency DAGs and forced execution ordering. | **CORRECT** |
| `jacobi.c` | Stencil Computation / `collapse(2)` | Validates double-buffered iterative algorithms and verifies loop collapsing without race conditions. | **CORRECT** |

---
## Results & Visualizations

### 1. Overall Model Accuracy by Prompting Strategy

![Benchmark Accuracy by Model](benchmark_accuracy.png)

#### Significance & Key Observations:
* **Frontier Model Consistency**: `gpt-5.4` achieved a perfect baseline performance (100.0% pass rate) under `naive.txt` prompting, while `gpt-4o` followed closely at 87.5%.
* **The "Few-Shot Degradation" Effect**: Counterintuitively, providing in-context reasoning examples (`few_shot.txt`) lowered performance for `gpt-3.5-turbo` (dropping from 87.5% to 62.5%) and `gpt-5.4` (dropping from 100.0% to 87.5%). Extended reasoning patterns often led models to over-analyze safe synchronization patterns (e.g., `barrier_correct.c`) and falsely flag them as buggy.
* **Open-Source Resilience**: `groq/qwen/qwen3.8-27b` saw a performance boost under `few_shot.txt` (rising from 75.0% to 87.5%), matching frontier models like `gpt-4o` once rate limit handling and output formatting were cleanly managed.

---

### 2. Test Case Pass Rate Across All Models

![Test Case Pass Rate Across All Models](testcase_pass_rate.png)

#### Significance & Key Observations:
* **Frontier Model Leadership**: `gpt-5.4` achieved the highest overall accuracy at **93.8%** (15/16), reaching a 100% pass rate under `naive.txt` prompting.
* **Prompt Strategy Nuance**: 
  * Few-shot prompting degraded performance for `gpt-3.5-turbo` (dropping from 87.5% to 62.5%) as the model tended to over-analyze safe synchronization patterns (e.g., `barrier_correct.c` and `task_depend_sync.c`).
  * `groq/qwen/qwen3.8-27b` benefited from structured few-shot examples, reaching an overall accuracy of **81.3%** (13/16).
  * Both `gpt-4o` (**87.5%**) and `gpt-4o-mini` (**75.0%**) demonstrated stable accuracy across both prompt strategies.

* **Scoping & Synchronization Blindspots**: `firstprivate_initialization.c` and `barrier_correct.c` proved to be the most challenging test cases across all models. LLMs frequently misinterpret whether private copies of variables modify the outer scope and struggle to correctly model `happens-before` relationships established by explicit barriers.

---

## Key Takeaways

1. **`gpt-5.4` Sets the Performance Baseline**
   - `gpt-5.4` demonstrated top-tier accuracy at **93.8%** overall (15/16), correctly identifying all 8 OpenMP patterns under naive prompting and failing only 1 case under few-shot prompting.

2. **Prompt Sensitivity Varies by Model Scale**
   - In-context examples (`few_shot.txt`) caused `gpt-3.5-turbo` to overfit on negative patterns, incorrectly flagging valid synchronization as buggy.
   - Conversely, `groq/qwen/qwen3.8-27b` performed better with structured few-shot examples, matching `gpt-4o` on the few-shot benchmark.

3. **Consistent Mid-Tier Reliability**
   - `gpt-4o` (**87.5%**) and `gpt-4o-mini` (**75.0%**) maintained identical accuracy across both naive and few-shot prompting modes, showing consistent handling of data races and OpenMP synchronization semantics.

---

## Accuracy Summary Table (8 Test Cases / 16 Total Runs per Model)

| Model | Naive Pass Rate | Few-Shot Pass Rate | Overall Accuracy |
| :--- | :---: | :---: | :---: |
| **gpt-5.4** | **100.0%** (8/8) | 87.5% (7/8) | **93.8%** (15/16) |
| **gpt-4o** | 87.5% (7/8) | 87.5% (7/8) | **87.5%** (14/16) |
| **groq/qwen/qwen3.8-27b** | 75.0% (6/8) | 87.5% (7/8) | **81.3%** (13/16) |
| **gpt-3.5-turbo** | 87.5% (7/8) | 62.5% (5/8) | **75.0%** (12/16) |
| **gpt-4o-mini** | 75.0% (6/8) | 75.0% (6/8) | **75.0%** (12/16) |

---

## Repository Structure

```bash
.
├── openmp/             # C code benchmark implementations & specification JSON
├── prompts/            # Prompt templates (naive.txt, few_shot.txt)
├── results/            # Saved raw text outputs per model execution
├── results.csv         # Aggregated benchmark evaluation logs
├── run_eval.py         # LiteLLM test runner
└── README.md
```

## Setting up the environment

Once you have cloned the repo, create a virtual environment

Then run: 

```bash
pip install -r requirements.txt
```

## Setting API keys in the terminal

Export any API keys to the terminal as follows:

```bash
export OPENAI_API_KEY="saerfserger......"
```

or

```bash
export GROQ_API_KEY="saerfserger......"
```

and so on.

## Running the Evaluation
To execute the benchmark against any supported model:

```bash
python run_eval.py --model gpt-4o --prompt-file naive.txt --code-file barrier_correct.c
```

Or through one of the shell scripts, for example:

```bash
models/openai/gpt_5.4.sh
```
