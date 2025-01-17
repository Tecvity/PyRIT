# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
import pathlib

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

from pyrit.common import path

nb_directory_path = pathlib.Path(path.DOCS_CODE_PATH, "converters").resolve()

# These notebooks will need to be re-run manually as they require human input
skipped_files = ["6_human_converter.ipynb"]


@pytest.mark.parametrize(
    "file_name",
    [file for file in os.listdir(nb_directory_path) if file.endswith(".ipynb") and file not in skipped_files],
)
def test_execute_notebooks(file_name):
    nb_path = pathlib.Path(nb_directory_path, file_name).resolve()
    with open(nb_path) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600)

    try:
        # Execute notebook, test will throw exception if any cell fails
        ep.preprocess(nb, {"metadata": {"path": nb_path.parent}})
    except Exception as e:
        pytest.fail(f"Notebook '{file_name}' failed to execute: {e}")
