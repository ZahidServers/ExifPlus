=========================
Installation Instructions
=========================

-----------------------
pip (Recommended Method)
-----------------------

Install ExifPlus from PyPI:

.. code-block:: bash

    pip install exifplus

Run it:

.. code-block:: bash

    exifplus

-----------------------------
pipx (Best for running as app)
-----------------------------

.. code-block:: bash

    pipx install exifplus
    exifplus

---------------------------------------------
Debian / Ubuntu / Kali / Parrot (PEP 668 note)
---------------------------------------------

If you see:

::

    error: externally-managed-environment

Use one of:

.. code-block:: bash

    pipx install exifplus

or:

.. code-block:: bash

    python3 -m venv venv
    source venv/bin/activate
    pip install exifplus

------------------------------------
Windows / macOS / Linux Requirements
------------------------------------

ExifPlus requires:

- Python 3.9+
- pyexiv2
- hachoir
- ttkbootstrap

Windows has limited support for metadata *editing* due to pyexiv2 backend issues.
