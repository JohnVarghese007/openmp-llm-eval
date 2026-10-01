from pathlib import Path
from datetime import datetime
import time
import subprocess
import argparse
import litellm
import csv
import json
import re


# Ground truth dictionary mapping C files to their true correctness
GROUND_TRUTH = {
    "critical_section.c": "CORRECT",
    "barrier_correct.c": "CORRECT",
    "drb_example.c": "INCORRECT",
    "flush_barrier_sync.c": "INCORRECT",
    "firstprivate_initialization.c": "INCORRECT",
    "single_nowait_barrier.c": "INCORRECT",
    "task_depend_sync.c": "CORRECT",
    "jacobi.c": "CORRECT",
}


def load_specs() -> dict:
    specs_path = Path("openmp/descriptions.json")
    if specs_path.exists():
        return json.loads(specs_path.read_text(encoding="utf-8"))
    return {}

def build_prompt(prompt_file: str, code_file: str) -> str:
    prompt_template = Path(f"prompts/{prompt_file}").read_text(encoding="utf-8")
    code = Path(f"openmp/{code_file}").read_text(encoding="utf-8")
    specs = load_specs()
    spec = specs.get(code_file, "Execute the program correctly and deterministically.")
    return prompt_template.replace("{SPECIFICATION}", spec).replace("{CODE}", code)


def run_model(model: str, prompt: str) -> str:
    """ Calls LiteLLM completion API to run the models across different providers. """

    """
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    )

    return result.stdout
    """

    #try and dodge rate limits
    #time.sleep(25)
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            # prompt=prompt
            max_tokens=500,
            num_retries=3
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        print(f"Error invoking model '{model}': {e}")
        return f"ERROR: {e}"


def parse_verdict(output: str) -> str:
    """ Extract Verdict from output text using strict word boundary matching. """
    # Search for "Verdict:" followed by CORRECT or INCORRECT
    match = re.search(r"VERDICT:\s*\b(CORRECT|INCORRECT)\b", output, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    # Fallback search for standalone word at the end of text
    match_fallback = re.search(r"\b(CORRECT|INCORRECT)\b\s*$", output.strip(), re.IGNORECASE)
    if match_fallback:
        return match_fallback.group(1).upper()
        
    return "UNKNOWN"


def log_to_csv(model: str, prompt_file: str, code_file: str, verdict: str):
    csv_path = Path("results.csv")
    file_exists = csv_path.exists()
    
    # Get true answer
    expected = GROUND_TRUTH.get(code_file, "UNKNOWN")
    # Evaluate if LLM was accurate
    is_accurate = "PASS" if verdict == expected else "FAIL"
    
    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Model", "PromptFile", "CodeFile", "PredictedVerdict", "GroundTruth", "Evaluation"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            model,
            prompt_file,
            code_file,
            verdict,
            expected,
            is_accurate
        ])


def save_result(model: str, prompt_file: str, code_file: str, output: str) -> Path:
    """ Saves the evaluation results to a file. """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model_name = (model.replace(":", "-").replace("/", "-"))
    result_dir = Path("results") / safe_model_name
    result_dir.mkdir(parents=True, exist_ok=True)

    prompt_name = Path(prompt_file).stem
    code_name = Path(code_file).stem
    output_file = (result_dir / f"{code_name}_{prompt_name}_{timestamp}.txt")
    metadata = f"""MODEL={model}
PROMPT={prompt_file}
CODE={code_file}
TIMESTAMP={timestamp}

========================================

"""
    output_file.write_text(metadata + output, encoding="utf-8")
    verdict = parse_verdict(output)
    log_to_csv(model, prompt_file, code_file, verdict)
    return output_file


def main():

    parser = argparse.ArgumentParser(
        description="Run OpenMP benchmark against an LLM"
    )

    parser.add_argument(
        "--model",
        default="ollama/qwen2.5-coder:3b",
        help="Model name"
    )

    parser.add_argument(
        "--prompt-file",
        default="naive.txt",
        help="Prompt template file in prompts/"
    )

    parser.add_argument(
        "--code-file",
        default="race_sum.c",
        help="Code file in openmp/"
    )

    args = parser.parse_args()

    final_prompt = build_prompt(
        args.prompt_file,
        args.code_file
    )

    output = run_model(
        args.model,
        final_prompt
    )

    print(output)

    output_path = save_result(
        args.model,
        args.prompt_file,
        args.code_file,
        output
    )

    print(f"\nSaved results to: {output_path}")
    print(f"Appended summary to results.csv")


if __name__ == "__main__":
    main()