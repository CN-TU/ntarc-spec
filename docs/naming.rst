Naming Conventions
==================

Paper Names
-----------

Each JSON file should be called ``data/papers/YEAR/LNAME_1STWORDS.json``, with ``YEAR`` the year of the paper, ``LNAME`` the main author's last name and ``1STWORDS`` for the first word (or first two/three words) of the title, and this filename should be completely lowercase.

Example filename: ``data/papers/2016/iglesias_timeactivity.json``

Feature Names
-------------

Feature names should in principle use the names defined in `IANA's website <http://www.iana.org/assignments/ipfix/ipfix.xhtml#ipfix-information-elements>`_.
However, IANA Information Elements do not cover all the features that can be extracted from packets.
If this is the case for a specific feature, there are two options:

    * If the feature is likely used by many other people: prefix the feature name with ``_`` (underscore), and add it to ``data/own_ies.csv``, if it is not already there.

    * If the feature is not likely to be used by other people: prefix the feature name ``__`` (double underscore). In this case, there is not need to add it to any list.

The naming convention in both cases should try to follow IANA's naming convention: feature names are to be descriptive and in camelcase.

Additionally, the the first case (with ``_``) can also be used for aliases; that is, features that are used a lot but that are some kind of combination of other features.
A list of aliases is defined in ``data/feature_aliases.json``.

Specification
-------------

Non-terminal Symbols
~~~~~~~~~~~~~~~~~~~~

Non-terminal symbols in the specification are lowercase words separated by ``-`` (hyphen).

Strings
~~~~~~~

Strings that are part of the specification are lowercase words separated by ``_`` (underscore).

Free text strings have no convention.
