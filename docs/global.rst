
Global rules 
============

In order to keep data curation homogeneity, some global rules must be defined. They are:

* The JSON files must use utf-8 encoding.
* ``null`` is a default value for fields that have not been checked in the curation process. 
* ``"missing"`` replaces ``null`` when the required information for a specific fields has been checked but not found in the paper.
* To avoid confusion, everything should be written in lower cases, even names and acronyms that are usually written in capitals; e.g., "tcp", "shakespeare". A relevant exception is the set of IANA IPFIX features.
* Any value that is not common or included among the predefined options must be preceded by '_', e.g., ``"_new_approach"``.
* Curated files must be named according to the following nomenclature: [first_author_surname]_[first_paper_title_word].json; e.g., *iglesias_time-activity.json*. More title words can be added to avoid matching. 
* Whenever a field allows an array of values, the name finishes with *s*. Otherwise, it only allows one value. For example:

.. code-block:: none

	"1st_author": "chekhov, a.",
	"authors": ["Chekhov, Anton", "de Maupassant, Guy", "Stifter, Adalbert"]

* Fields are established according to two granularity levels for the curation process: *basic* and *complete*. Second level fields are distinguished by an "(*optional*)" next to their name. First level fields (basic, priority) are all the remaining fields, which are mandatory.
* Additional fields for human readability can be added (e.g., for leaving comments), and the name of this field should be preceded by '_', e.g., ``"_comment"``.
* The information in each main block is always to be taken in its context.
  For example, when looking at whether the data is ``"raw"`` or ``"preprocessed"`` in the Data block, consider the state of the data before the preprocessing phase.
* In addition to the documentation, please check the supporting examples and templates for clarification:

  * *example_basic.json*
  * *example_complete.json*
  * *template_basic.json*
  * *template_complete.json*

