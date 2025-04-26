#!/bin/bash
cd ..
pip install -r requirements/requirements_dev.txt
pip install -e .
nbstripout --install
nbdime config-git --enable