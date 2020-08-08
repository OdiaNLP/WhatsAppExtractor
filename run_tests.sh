black -l 99 -t py38 wextractor tests
coverage run --source=wextractor  -m pytest tests -vv -s --pdb && coverage html -i
