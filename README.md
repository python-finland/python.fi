Introduction
------------

This is web site source code for Python Finland, http://python.fi.

All source code is licensed under `BSD license <http://www.opensource.org/licenses/bsd-license.php>`_.

Web site template is from http://freehtml5templates.com

Repos
-----

The official source code repository is
https://github.com/python-finland/python.fi.

Getting started
---------------

Commands::

    git clone git@github.com:python-finland/python.fi.git
    cd python.fi
    virtualenv venv
    venv/bin/pip install Lektor

Running development server
--------------------------

Example::

    cd python.fi/pythonfi
    ../venv/bin/lektor server

Deploy
------

Example::

    cd python.fi/pythonfi
    ../venv/bin/lektor build --output-path output
    scp -r output python.fi:python.fi

Contact
-------

Regarding any questions please contact the `board members
<hallitus@python.fi>`_ of the Python Finland association, or the
`PIG-Fi mailing list <http://groups.google.com/group/pigfi>`_.
