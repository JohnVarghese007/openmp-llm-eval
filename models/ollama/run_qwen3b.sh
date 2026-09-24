#!/bin/bash

# Ensure your OpenAI API key is set before running
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set."
    echo "Please set it using: export OPENAI_API_KEY='your-api-key'"
    exit 1
fi

MODEL="ollama_chat/qwen2.5-coder:3b"

BENCHMARKS=(
    
    #race_sum.c
    #shared_counter.c
    #shared_array_update.c
    #check_then_act.c
    #loop_dependency.c
    ##missing_barrier.c
    #reduction_sum.c
    #atomic_counter.c
    critical_section.c
    #private_variable.c
    barrier_correct.c
    drb_example.c
    flush_barrier_sync.c
    firstprivate_initialization.c
    single_nowait_barrier.c
    task_depend_sync.c
)

PROMPTS=(
    naive.txt
    few_shot.txt
)

for prompt in "${PROMPTS[@]}"
do
    echo "====================================="
    echo "Running $prompt Benchmarks with $MODEL"
    echo "====================================="
    for bench in "${BENCHMARKS[@]}"
    do
        echo "Processing $bench..."
        python run_eval.py \
            --model "$MODEL" \
            --prompt-file "$prompt" \
            --code-file "$bench"
    done
done

echo "Done."