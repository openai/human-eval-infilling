import os

import pkg_resources
from setuptools import find_packages, setup

setup(
    name="human-eval-infilling",
    py_modules=["human_eval_infilling"],
    version="1.0",
    description="",
    author="OpenAI",
    packages=find_packages(),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    entry_points={
        "console_scripts": [
            "evaluate_infilling_functional_correctness = human_eval_infilling.evaluate_functional_correctness",
        ]
    },
)
