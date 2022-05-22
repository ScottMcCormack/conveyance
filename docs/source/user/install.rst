.. _install:

Installation of conveyance
==========================

This part of the documentation covers the installation of conveyance.
The first step to using any software package is getting it properly installed.


$ python -m pip install conveyance
----------------------------------

To install conveyance, simply run this simple command in your terminal of choice::

    $ python -m pip install conveyance

Get the Source Code
-------------------

conveyance is actively developed on GitHub, where the code is
`always available <https://github.com/ScottMcCormack/conveyance>`_.

You can either clone the public repository::

    $ git clone git://github.com/ScottMcCormack/conveyance.git

Or, download the `tarball <https://github.com/ScottMcCormack/Conveyance/tarball/main>`_::

    $ curl -OL https://github.com/ScottMcCormack/Conveyance/tarball/main
    # optionally, zipball is also available (for Windows users).

Once you have a copy of the source, you can embed it in your own Python
package, or install it into your site-packages easily::

    $ cd conveyance
    $ python -m pip install .
