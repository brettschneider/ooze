#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1
mkdir test_results 2> /dev/null
pytest --cov=. --junitxml=test_results/output.xml -v -p no:cacheprovider && \
    coverage html -d test_results/html && \
    coverage xml -o test_results/coverage.xml
