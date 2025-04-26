#!/bin/bash

python3 src/main.py "/Static-Site-Generator/"
cd docs && python3 -m http.server 8888