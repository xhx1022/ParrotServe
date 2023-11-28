# Copyright (c) 2023 by Microsoft Corporation.
# Author: Chaofan Lin (v-chaofanlin@microsoft.com)

# Functions in this file are used for immitating the workload of chain summarization.

# Reference of prompt length: https://python.langchain.com/docs/use_cases/summarization

import parrot as P

fake_long_document_chunk = "Test " * 650  # len=650 for each chunk
refine_instruction = "Test " * 10


def chain_sum_test(
    previous_document: P.Input,
    refined_document: P.Output(
        P.SamplingConfig(ignore_tokenizer_eos=True, max_gen_length=20)
    ),  # 20 Gen
):
    pass


"""
A long chunked doc, a previous (refined) doc, and some instructions.
"""

chain_sum_test_body = (
    f"{fake_long_document_chunk}"
    + "{{previous_document}}"
    + f"{refine_instruction}"
    + "{{refined_document}}"
)

chain_sum_test.__doc__ = chain_sum_test_body
chain_sum_test = P.semantic_function(cache_prefix=False)(chain_sum_test)

# print(chain_sum_test_body)
