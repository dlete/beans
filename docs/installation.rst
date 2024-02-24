Requirements In your laptop/pc
==============================
You need 
- ``git``
- ``Python 3``


To setup your laptop/pc to work on this project
===============================================
#. Create a virtual environment for this project
#. Change your Python environment to the project environment
#. Create a project directory::

    mk dir <project_dir>

#. Clone the source. Take the ``main`` branch::

    git clone <url>

#. Install the Python packages required for the project::

    pip install ./requirements.txt



Working method
==============
Create a ``git`` working/temporal/own branch for any changes you want to implement::

    git checkout -b <working branch>


Commit changes in working branch::

    git status
    git add --all .
    git commit -m "<comment>"


Merge to ``master``::

    git checkout master
    git merge <working_branch>
