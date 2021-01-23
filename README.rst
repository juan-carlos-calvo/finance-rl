========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/finance-rl/badge/?style=flat
    :target: https://readthedocs.org/projects/finance-rl
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/juan-carlos-calvo/finance-rl.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/juan-carlos-calvo/finance-rl

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/juan-carlos-calvo/finance-rl?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/juan-carlos-calvo/finance-rl

.. |requires| image:: https://requires.io/github/juan-carlos-calvo/finance-rl/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/juan-carlos-calvo/finance-rl/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/juan-carlos-calvo/finance-rl/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/juan-carlos-calvo/finance-rl

.. |version| image:: https://img.shields.io/pypi/v/liquidation-gym.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/liquidation-gym

.. |wheel| image:: https://img.shields.io/pypi/wheel/liquidation-gym.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/liquidation-gym

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/liquidation-gym.svg
    :alt: Supported versions
    :target: https://pypi.org/project/liquidation-gym

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/liquidation-gym.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/liquidation-gym

.. |commits-since| image:: https://img.shields.io/github/commits-since/juan-carlos-calvo/finance-rl/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/juan-carlos-calvo/finance-rl/compare/v0.0.0...master



.. end-badges

gym env simulating a liquidation of assets

* Free software: Apache Software License 2.0

Installation
============

::

    pip install liquidation-gym

You can also install the in-development version with::

    pip install https://github.com/juan-carlos-calvo/finance-rl/archive/master.zip


Documentation
=============


https://finance-rl.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
