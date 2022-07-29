import sys

import fire

from human_eval_infilling.evaluation import evaluate_functional_correctness


def entry_point(
    benchmark_name: str,
    sample_file: str,
    k: str = "1,10,100",
    n_workers: int = 4,
    timeout: float = 3.0,
):
    """
    Evaluates the functional correctness of generated samples, and writes
    results to f"{sample_file}_results.jsonl.gz"

    :param benchmark_name: could be one of "single-line", "multi-line", "random-span", "random-span-light"
    """
    k = list(map(int, k.split(",")))
    results = evaluate_functional_correctness(benchmark_name, sample_file, k, n_workers, timeout)
    print(results)


def main():
    fire.Fire(entry_point)


sys.exit(main())
