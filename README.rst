.. contents:: Table of Contents


Introduction
============

This package is used to extract files and directories
from a zip file and add them to a Plone application.

The module provides a view showing the contents of the
zip file and the associated file sizes. From the view you
can extract everything from the file or select a subset of elements
to extract.

The extraction itself is designed to be as safe as possible, notably:

* Safe against zip bombs

  * Checks announced size of files to extract (from zip file header) and stops extracting if that size is exceeded.
  * We can also set a total maximum data volume allowed to be extracted.

* Safe against extraction outside of destination folder.

* Controlled RAM usage. Uses a buffer to write to a temporary file.

* Handles things like zip file containing several files with the same name.

Compatibility
-------------

Plone 4.3.x

Implementation
==============

- The ``ftw.zipextract.zipextracter.ZipExtracter`` class handles the extraction from the zip file.
- The ``ftw.zipextract.browser.zipextract_view.ZipExtractView`` is used for the rendering of the extraction view. It is registered as ``zipextract`` and will be applied on its context.

Handling and creation of files and folders depends on the context and the content types. To handle this, 4 interfaces are used:

- ``ftw.zipextract.interfaces.IFile`` defines a few methods for file handling and notably an `is_zip` method used to determine whether the extraction can be used on a given file or not.
- ``ftw.zipextract.interfaces.IFactoryTypeDecider`` decides which factory type information to use for creating folders or files from the zip within a specific container.

    - defines a ``get_file_fti`` method
    - defines a ``get_folder_fti`` method

- ``ftw.zipextract.interfaces.IFileCreator`` defines a ``create`` method to create a new file
- ``ftw.zipextract.interfaces.IFolderCreator`` defines a ``create`` method to create a new folder

Adapting the package to your application
----------------------------------------

To adapt this package to other applications you might need to write adapters for the 4 interfaces described above. ``ftw.zipextract`` provides default implementations for Dexterity types and Archetypes for all 4 interfaces.


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.zipextract

Install the generic setup profile of ``ftw.zipextract``.


Development
===========

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python bootstrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.zipextract
- Issues: https://github.com/4teamwork/ftw.zipextract/issues
- Pypi: http://pypi.python.org/pypi/ftw.zipextract


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.zipextract`` is licensed under GNU General Public License, version 2.
