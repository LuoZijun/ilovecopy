
.. contents::


Requirements
---------------

GNU/Linux:

.. code:: bash
    
    # Debian/Ubuntu
    sudo apt install python35 python3-pip
    # Redhat/Fedora/OpenSuse
    sudo yum install python35 python3-pip

    sudo pip3 install aiohttp Pillow


macOS:

.. code:: bash
    
    brew install python35
    pip3 install aiohttp Pillow


Run
------

.. code:: bash
    
    # Download images
    python3 spider.py
    # python3 spider.py | grep 'ERROR'

    # Merge (long time ...)
    python3 merge.py

