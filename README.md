PyContacts
==========
PyContacts is a little project made with Python, Pyramid web framework and Jinja2.

Installing and Running (on Linux)
---------------------------------

- Set an environment variable: $ export VENV=~/my_path/env
- Create a virtual environment: $ python3 -m venv $VENV
- Clone this repository: $ git clone https://github.com/Igorolivei/pycontacts.git
- Run setup.py: $ $VENV/bin/pip install -e .
- Initialize PyContacts using development.ini: $ $VENV/bin/pserve development.ini --reload

* To run tests, execute: $VENV/bin/py.test contact_book/tests.py -q