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
     - Mount and drag to Applications. On first launch, go to
       **System Settings → Privacy & Security → Open Anyway**
       if macOS blocks the app.
   * - Linux
     - ``PyGRA-linux.tar.gz``
     - Extract and run ``./PyGRA/PyGRA`` directly.
   * - Windows
     - ``PyGRA.exe``
     - Run directly. Windows may show a SmartScreen warning —
       click **More info → Run anyway**.

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
