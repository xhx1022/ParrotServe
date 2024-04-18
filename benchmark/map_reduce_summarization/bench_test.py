# Copyright (c) 2023 by Microsoft Corporation.
# Author: Chaofan Lin (v-chaofanlin@microsoft.com)


import time
import asyncio

import parrot as P
from parrot.utils import cprofile
from parrot.testing.localhost_server_daemon import fake_core_server

vm = P.VirtualMachine(os_http_addr="http://localhost:9000", mode="debug")

map_lowupperbound = vm.import_function(
    "map_sum_test_baseline",
    module_path="benchmark.workloads.test_examples.map_reduce_summarization",
)
map_highupperbound = vm.import_function(
    "map_sum_test_main",
    module_path="benchmark.workloads.test_examples.map_reduce_summarization",
)
reduce_func_test = vm.import_function(
    "reduce_sum_test_15",
    module_path="benchmark.workloads.test_examples.map_reduce_summarization",
)

chunk_num = len(reduce_func_test.inputs)

map_document_chunk = "Test " * 1000  # len=1000 for each chunk


async def _preprocess(map_func):
    coroutines = []
    for _ in range(chunk_num):
        coroutines.append(map_func.ainvoke(map_document_chunk))
    # time.sleep(0.1)
    chunk_sums = await asyncio.gather(*coroutines)
    return chunk_sums


async def main():
    chunk_sums = await _preprocess(map_highupperbound)
    final_output = reduce_func_test(*chunk_sums)
    final_output.get()


async def baseline():
    chunk_sums = await _preprocess(map_lowupperbound)
    final_output = reduce_func_test(*chunk_sums)
    final_output.get()


def test_baseline():
    print("baseline:")
    # with cprofile("baseline"):
    print("Time: ", vm.run(baseline, timeit=True))
    time.sleep(3)


def test_main():
    print("main:")
    # with cprofile("main"):
    print("Time: ", vm.run(main, timeit=True))
    time.sleep(3)


if __name__ == "__main__":
    # test_baseline()
    # test_main()

    for _ in range(10):
        # test_baseline()
        test_main()