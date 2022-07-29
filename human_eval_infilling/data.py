import gzip
import json
import os
from typing import Dict, Iterable

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def read_problems(benchmark_name: str) -> Dict[str, Dict]:
    benchmark_file = {
        "single-line": os.path.join(ROOT, "HumanEval-SingleLineInfilling.jsonl.gz"),
        "multi-line": os.path.join(ROOT, "HumanEval-MultiLineInfilling.jsonl.gz"),
        "random-span": os.path.join(ROOT, "HumanEval-RandomSpan.jsonl.gz"),
        "random-span-light": os.path.join(ROOT, "HumanEval-RandomSpanLight.jsonl.gz"),
        "test": os.path.join(ROOT, "example_problem.jsonl"),
    }[benchmark_name]
    return {task["task_id"]: task for task in stream_jsonl(benchmark_file)}


def stream_jsonl(filename: str) -> Iterable[Dict]:
    """
    Parses each jsonl line and yields it as a dictionary
    """
    if filename.endswith(".gz"):
        with open(filename, "rb") as gzfp:
            with gzip.open(gzfp, "rt") as fp:
                for line in fp:
                    if any(not x.isspace() for x in line):
                        yield json.loads(line)
    else:
        with open(filename, "r") as fp:
            for line in fp:
                if any(not x.isspace() for x in line):
                    yield json.loads(line)


def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False):
    """
    Writes an iterable of dictionaries to jsonl
    """
    if append:
        mode = "ab"
    else:
        mode = "wb"
    filename = os.path.expanduser(filename)
    if filename.endswith(".gz"):
        with open(filename, mode) as fp:
            with gzip.GzipFile(fileobj=fp, mode="wb") as gzfp:
                for x in data:
                    gzfp.write((json.dumps(x) + "\n").encode("utf-8"))
    else:
        with open(filename, mode) as fp:
            for x in data:
                fp.write((json.dumps(x) + "\n").encode("utf-8"))
