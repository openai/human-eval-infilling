# HumanEval Infilling Benchmarks

This is an evaluation harness for the HumanEval infilling benchmarks described in the [FIM paper](https://arxiv.org/abs/2207.14255).

## Installation

Make sure to use python 3.7 or later:
```
$ conda create -n codex python=3.7
$ conda activate codex
```

Check out and install this repository:
```
$ git clone https://github.com/openai/human-eval-infilling
$ pip install -e human-eval-infilling
```

## Usage

**This program exists to run untrusted model-generated code. Users are strongly
encouraged not to do so outside of a robust security sandbox. The [execution
call](https://github.com/openai/human-eval-infilling/blob/master/human_eval_infilling/execution.py#L74-L84)
in `execution.py` is deliberately commented out to ensure users read this
disclaimer before running code in a potentially unsafe manner. See the comment in
`execution.py` for more information and instructions.**

After following the above instructions to enable execution, generate samples
and save them in the following JSON Lines (jsonl) format, where each sample is
formatted into a single line like so:
```
{"task_id": "Corresponding task ID from the desired benchmark", "completion": "Completion only without the prompt"}
```
Ensure that the `task_id` used matches the `task_id` from the desired benchmark. See below and the paper for information on the benchmarks available.

We provide `example_problem.jsonl` and `example_solutions.jsonl` under `data`
to illustrate the format and help with debugging.

Here is nearly functional example code (you just have to provide
`generate_one_completion` to make it work) that saves generated completions for
the single-line infilling benchmark to `samples.jsonl`.
```
from human_eval_infilling.data import write_jsonl, read_problems

problems = read_problems(benchmark_name="single-line")

num_samples_per_task = 100
samples = [
    dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"], problems[task_id]["suffix"]))
    for task_id in problems
    for _ in range(num_samples_per_task)
]
write_jsonl("samples.jsonl", samples)
```

To evaluate the samples, run
```
$ evaluate_infilling_functional_correctness samples.jsonl --benchmark_name=single-line
Reading samples...
103300it [00:01, 23787.50it/s]
Running test suites...
100%|...| 103300/103300 [16:11<00:00, 33.76it/s]
Writing results to samples.jsonl_results.jsonl...
100%|...| 103300/103300 [00:00<00:00, 42876.84it/s]
{'pass@1': ..., 'pass@10': ..., 'pass@100': ...}
```
This script provides more fine-grained information in a new file ending in
`<input_path>_results.jsonl`. Each row now contains whether the completion
`passed` along with the execution `result` which is one of "passed", "timed
out", or "failed".

As a quick sanity-check, the example samples should yield 30% pass@1.
```
$ evaluate_infilling_functional_correctness data/example_samples.jsonl --benchmark_name=test
Reading samples...
10it [00:00, 3365.94it/s]
100%|...| 10/10 [00:03<00:00,  2.76it/s]
Writing results to data/example_samples.jsonl_results.jsonl...
100%|...| 10/10 [00:00<00:00, 1309.08it/s]
{'pass@1': 0.30000000000000004, 'pass@10': 1.0}
```

There are 4 available benchmarks: single-line, multi-line, random-span, random-span-light. The first two are introduced in the [InCoder paper](https://arxiv.org/abs/2204.05999) and the latter two are introduced in the [FIM paper](https://arxiv.org/abs/2207.14255). All benchmarks are used extensively in the FIM paper. There is also a dummy benchmark for testing.

Because there is no unbiased way of estimating pass@k when there are fewer
samples than k, the script does not evaluate pass@k for these cases. To
evaluate with other k values, pass `--k=<comma-separated-values-here>`. For
other options, see
```
$ evaluate_infilling_functional_correctness --help
```
However, we recommend that you use the default values for the rest.

## Known Issues

While evaluation uses very little memory, you might see the following error
message when the system is running out of RAM. Since this may cause some
correct programs to fail, we recommend that you free some memory and try again.
```
malloc: can't allocate region
```
