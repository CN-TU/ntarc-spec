.. _reference:

Reference
=========

Properties
``````````

title
~~~~~

(*string*) The title of the paper.

.. code-block:: none

     "title": "time-activity footprints in ip traffic"

1st_author
~~~~~~~~~~

(*string*) First author name and surname with format: *surname, n.*.

.. code-block:: none

     "1st_author": "chekhov, a."
 
authors
~~~~~~~

(*array* of *strings*)  Array with the authors' list. Format as in BibTeX. Check `this StackExchange thread <https://tex.stackexchange.com/questions/557/how-should-i-type-author-names-in-a-bib-file>`_ for details.

.. code-block:: none

     "authors": ["Chekhov, Anton", "de Maupassant, Guy", "Stifter, Adalbert"]

Example with only one author:

.. code-block:: none
 
 	"authors": ["Chekhov, Anton"]

publication_name
~~~~~~~~~~~~~~~~

(*string*) Name of the publication (journal or conference). Please, use the most common name used in scientific citations (without abbreviations and in lower case). Example:

.. code-block:: none

     "publication_name": "ieee transactions on networking"

publication_type
~~~~~~~~~~~~~~~~
(*string*) It marks the type of publication. Please, consider carefully if the publication fits any of the following default labels (values):

* ``"peer_reviewed_journal"``
  journal with a peer review process.
* ``"peer_reviewed_conference"``
  conference with a peer review process.
* ``"arxiv"``
  paper is published only in arxiv.
* ``"technical_report"``
  technical report, usually without peer review, and published in the author's/university's page.

Example:

.. code-block:: none
 
 	"publication_type": "peer_reviewed_journal"

year
~~~~
(*numerical*) The year of the publication release. Example:

   .. code-block:: none
 
 	"year": 2016

organization_publishers (*optional*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(*array* of *strings*) Please, consider carefully if the publication fits one or more of the following default organizations (values):

* ``"ieee"``
* ``"elsevier"``
* ``"acm"``
* ``"springer"``
* ``"wiley"``
* ``"taylor_&_francis"``
* ``"mdpi"``

Example:

.. code-block:: none
 
 	"organization_publishers": ["acm"]


pages_number_of (*optional*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(*numerical*) The total number of pages of the paper. Example:

.. code-block:: none
 
 	"pages_number_of": 8

bibtex
~~~~~~

(*object*) Various BibTeX-related fields. This object supports extra fields, so you are free to add other BibTeX properties. All fields in this object are strings.

type
````

(*string*, for *bibtex* citation compatibility) Please, consider carefully if the publication fits one or more of the following default bibtex types (values):

* ``"article"``
* ``"inproceedings"``
* ``"techreport"``
* ``"inbook"``
* ``"misc"``

Example:

.. code-block:: none
 
 	"type": "article"


volume
``````

(*string*, for *bibtex* citation compatibility) The volume of the related multi-volume publication or book. If there is no volume, write ``"missing"``. Example:

.. code-block:: none
 
 	"volume": "8"

issue
`````

(*string*, for *bibtex* citation compatibility) The issue or number of the related publication or book. If there is no issue or number, write ``"missing"``. Example:

.. code-block:: none
 
 	"issue": "5"

pages
`````

(*string*, for *bibtex* citation compatibility) The page range of the paper. If there is no page range, write ``"missing"``. Write "--" between page numbers. Example:

.. code-block:: none
 
 	"pages": "102--114"

access_open (*optional*)
~~~~~~~~~~~~~~~~~~~~~~~~

(*boolean*) Is the paper open access for any normal Internet user? Example:

.. code-block:: none
 
 	"access_open": true

curated_by
~~~~~~~~~~

(*string*) Last person who reviewed/curated/modified this JSON file. Example:

.. code-block:: none
 
 	"curated_by": "ferreira, d."

curated_last_revision
~~~~~~~~~~~~~~~~~~~~~

(*string*, format: *dd-mm-yyyy*) Date of the last revision/modification of this JSON file. Example:

.. code-block:: none
 
 	"curated_last_revision": "10-01-2017"

curated_revision_number
~~~~~~~~~~~~~~~~~~~~~~~

(*numerical*) Number of the total revisions/modification/updates carried out on this specific JSON file. Minimum number is 1. Example:

.. code-block:: none
 
 	"curated_revision_number": 3



JSON example (reference, complete)
``````````````````````````````````

.. code-block:: none

  "reference": {
    "title": "time-activity footprints in ip traffic", 
    "1st_author": "iglesias, f.", 
    "authors": ["Iglesias, F\'elix", "Zseby, Tanja"],
    "publication_name": "computer networks",
    "publication_type": "peer_reviewed_journal",
    "year": 2016,
    "organization_publishers": ["elsevier"],
    "pages_number_of": "12",
    "bibtex": {
      "type": "article",
      "volume": "107, Part 1",
      "issue": "missing",
      "pages": "64--75"
    },
    "access_open": false,
    "curated_by": "iglesias, f.",
    "curated_last_revision": "10-04-2017",
    "curated_revision_number": 2
  } 

