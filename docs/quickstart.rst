QuickStart
==========

Installation
------------

.. code-block:: shell

   $ pip install chouseisan_py

Usage
-----

.. code-block:: pycon

    >>> from datetime import datetime
    >>> from chouseisan_py.chouseisan import Auth, Chouseisan
    >>> auth = Auth(email="test@example.com", password="<secret>")
    >>> chouseisan = Chouseisan(auth)
    >>> chouseisan.create_event(
    ...    title="test event",
    ...    candidate_days=[datetime(2021, 10, 17, 19, 0), datetime(2021, 10, 18, 19, 0)]
    ... )
    'https://chouseisan.com/s?h=f7b7fc11995b441782844bc3fddaf456'
