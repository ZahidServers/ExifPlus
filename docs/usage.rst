=====
Usage
=====

-------------------
Launching ExifPlus
-------------------

Run from terminal:

.. code-block:: bash

    exifplus

or:

.. code-block:: bash

    python -m exifplus

--------------------
Opening Media Files
--------------------

When you click **Open**, ExifPlus gives two choices:

1. **Local File**  
   Choose a JPG/PNG/TIFF/HEIC or MP4/MOV/MKV/AVI.

2. **From URL**  
   Paste a URL and ExifPlus downloads the file for inspection.

Supported formats:

- Images: ``.jpg``, ``.jpeg``, ``.png``, ``.tiff``, ``.heic``
- Videos: ``.mp4``, ``.mov``, ``.avi``, ``.mkv``

Notes:

- Some services (e.g., Blogger) strip EXIF metadata.
- Some sites block downloads (403 hotlink protection).

-----------------------
Viewing and Editing Data
-----------------------

- Double-click a cell to edit its value.
- Right-click for context menu:
  - Delete row
  - Add row below (EXIF/IPTC/XMP)

---------------------
Saving Edited Metadata
---------------------

Click **Save Metadata**.

Windows users:  
PyExiv2 editing backend is unstable; editing may not work. Linux/macOS recommended.

-------------------
Exporting Metadata
-------------------

Two export options:

- **CSV file**
- **JSON file**

---------------------
HTML Report Generator
---------------------

Click **Generate Report** to create a professional HTML report containing:

- Side-by-side image preview  
- Full metadata table  
- Clean formatting for:
  - Bugcrowd submissions  
  - HackerOne reports  
  - Forensics / OSINT  
