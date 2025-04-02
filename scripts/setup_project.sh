#!/bin/bash
cd ..
pip install -e .
nbstripout --install
nbdime config-git --enable