Download
========

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

Since PyGRA is not signed with an Apple Developer certificate, macOS may
block it on first launch with the message *"Apple cannot verify that PyGRA
does not contain malware"*. To open it:

1. Open **System Settings → Privacy & Security**
2. Scroll down to the Security section
3. Click **"Open Anyway"** next to the PyGRA message
4. Confirm by clicking **"Open"** in the dialog that appears

This is a one-time step — subsequent launches will open normally.

Windows security note
---------------------

Windows SmartScreen may show a warning when running ``PyGRA.exe`` for the
first time, since the app is not signed with a Microsoft certificate:

1. Click **"More info"**
2. Click **"Run anyway"**

This is a one-time step.
