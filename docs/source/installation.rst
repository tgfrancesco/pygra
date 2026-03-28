Installation
============

Download
--------

Pre-built installers are available on the
`Releases page <https://github.com/tgfrancesco/PyGRA/releases/latest>`_
— no Python installation required.

.. list-table::
   :widths: 15 30 55
   :header-rows: 1

   * - Platform
     - File
     - Notes
   * - macOS
     - ``PyGRA-macos.dmg``
     - Open the DMG, drag **PyGRA** to the **Applications** folder.
       On first launch macOS may block the app — see :ref:`macos-security` below.
   * - Linux
     - ``PyGRA-linux.tar.gz``
     - Extract and run ``./PyGRA/PyGRA`` directly.
   * - Windows
     - ``PyGRA.exe``
     - Run directly. Windows may show a SmartScreen warning —
       click **More info → Run anyway**.

.. _macos-security:

macOS security note
-------------------

Since PyGRA is not signed with an Apple Developer certificate, macOS may block
it on first launch with the message *"Apple cannot verify that PyGRA does not
contain malware"*. To open it:

1. Open **System Settings → Privacy & Security**
2. Scroll down to the Security section
3. Click **"Open Anyway"** next to the PyGRA message
4. Confirm by clicking **"Open"** in the dialog that appears

This is a one-time step — subsequent launches will open normally.

Developer installation
----------------------

If you want to run PyGRA from source or contribute to the project,
install it in a Python environment.

Requirements
~~~~~~~~~~~~

- Python >= 3.11
- numpy >= 1.24
- scipy >= 1.10
- matplotlib >= 3.7
- PyQt5 >= 5.15

With conda (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   conda env create -f environment.yml
   conda activate pygra

Or install into an existing environment (e.g. your oxDNA environment):

.. code-block:: bash

   conda activate oxdna
   pip install -e .

With pip
~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt
   pip install -e .

Linux: dock/launcher icon
--------------------------

Run the provided install script once after installation to register the icon
and add PyGRA to the application launcher:

.. code-block:: bash

   bash install_icon_linux.sh

This copies the icon to ``~/.local/share/icons`` and creates a ``.desktop``
file in ``~/.local/share/applications``. You may need to log out and back in
for the icon to appear in the dock.

Running the tests
-----------------

.. code-block:: bash

   python -m pytest tests/ -q

.. note::
   On Linux, always use ``python -m pytest`` rather than ``pytest`` directly,
   to ensure the correct Python environment is used.
