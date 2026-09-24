from pathlib import Path
from datetime import datetime
import subprocess
import argparse
import litellm


def build_prompt(prompt_file: str, code_file: str) -> str:
    prompt_template = Path(f"prompts/{prompt_file}").read_text(encoding="utf-8")
    code = Path(f"openmp/{code_file}").read_text(encoding="utf-8")
    return prompt_template.replace("{CODE}", code)


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
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}]
            # prompt=prompt
            # max_tokens=2048
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        print(f"Error invoking model '{model}': {e}")
        return f"ERROR: {e}"


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

    print(
        f"\nSaved results to: {output_path}"
    )


if __name__ == "__main__":
    main()