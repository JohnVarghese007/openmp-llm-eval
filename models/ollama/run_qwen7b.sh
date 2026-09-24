#!/bin/bash

MODEL="ollama_chat/qwen2.5-coder:7b"

BENCHMARKS=(
    race_sum.c
    shared_counter.c
    shared_array_update.c
    check_then_act.c
    loop_dependency.c
    missing_barrier.c
    reduction_sum.c
    atomic_counter.c
    critical_section.c
    private_variable.c
    barrier_correct.c
)

PROMPTS=(
    naive.txt
    few_shot.txt
)

for prompt in "${PROMPTS[@]}"
do
    echo "====================================="
    echo "Running $prompt Benchmarks"
    echo "====================================="
    for bench in "${BENCHMARKS[@]}"
    do
        python run_eval.py \
            --model "$MODEL" \
            --prompt-file "$prompt" \
            --code-file "$bench"
    done
done

echo "Done."