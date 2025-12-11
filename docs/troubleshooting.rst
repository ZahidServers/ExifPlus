==============
Troubleshooting
==============

-----------------------
403 Errors on URL Input
-----------------------

Some websites block programmatic downloads (hotlink protection).  
Open the image in a browser and save manually.

-----------------------
Missing EXIF Metadata
-----------------------

CDNs often remove metadata. Use the original unprocessed file.

-----------------------------
pyexiv2 crashes on Windows
-----------------------------

Windows support for modifying metadata is limited.  
Viewing still works; editing works best on Linux/macOS.

----------------------------
PEP 668 installation failure
----------------------------

Use:

.. code-block:: bash

    pipx install exifplus

or:

.. code-block:: bash

    python3 -m venv venv
    source venv/bin/activate
