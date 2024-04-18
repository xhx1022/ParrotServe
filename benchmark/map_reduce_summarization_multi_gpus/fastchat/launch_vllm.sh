#!/bin/sh

python3 -m fastchat.serve.controller &

sleep 1

CUDA_VISIBLE_DEVICES=0 python3 -m fastchat.serve.vllm_worker \
    --model-path lmsys/vicuna-7b-v1.3 \
    --model-names "gpt-3.5-turbo" \
    --limit-worker-concurrency 9999 \
    --tokenizer hf-internal-testing/llama-tokenizer \
    --max-num-batched-tokens 2560 \
    --seed 0 \
    --port 21002 &

sleep 20

CUDA_VISIBLE_DEVICES=1 python3 -m fastchat.serve.vllm_worker \
    --model-path lmsys/vicuna-7b-v1.3 \
    --model-names "gpt-3.5-turbo" \
    --limit-worker-concurrency 9999 \
    --tokenizer hf-internal-testing/llama-tokenizer \
    --max-num-batched-tokens 2560 \
    --seed 0 \
    --port 21003 &

sleep 20

CUDA_VISIBLE_DEVICES=2 python3 -m fastchat.serve.vllm_worker \
    --model-path lmsys/vicuna-7b-v1.3 \
    --model-names "gpt-3.5-turbo" \
    --limit-worker-concurrency 9999 \
    --tokenizer hf-internal-testing/llama-tokenizer \
    --max-num-batched-tokens 2560 \
    --seed 0 \
    --port 21004 &

sleep 20

CUDA_VISIBLE_DEVICES=3 python3 -m fastchat.serve.vllm_worker \
    --model-path lmsys/vicuna-7b-v1.3 \
    --model-names "gpt-3.5-turbo" \
    --limit-worker-concurrency 9999 \
    --tokenizer hf-internal-testing/llama-tokenizer \
    --max-num-batched-tokens 2560 \
    --seed 0 \
    --port 21005 &

sleep 20

python3 -m fastchat.serve.openai_api_server --host localhost --port 8000 &
