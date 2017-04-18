
Global rules 
============

In order to keep data curation homogeneity, some global rules must be defined. They are:

* ``null`` is a default value for fields that have not been checked in the curation process. 
* ``"missing"`` replaces ``null`` when the required information for a specific fields has been checked but not found in the paper.
* To avoid confusion, everything should be written in lower cases, even names and acronyms that are usually written in capitals; e.g., "tcp", "shakespeare". A relevant exception is the set of IANA IPFIX features.
* Any value that is not common or included among the predefined options must be preceded by '_', e.g., ``"_new_approach"``.
* Curated files must be named according to the following nomenclature: [first_author_surname]_[first_paper_title_word].json; e.g., *iglesias_time-activity.json*. More words can be added to avoid matching. 
* Whenever a field allows an array of values, the name finishes with *s*. Otherwise, it only allows one value. For example:

.. code-block:: none

	"1st_author": "chejov, a.",
	"authors": ["chejov, a.","de_maupassant, g.","stifter, a."]

* Fields are established according to two granularity levels for the curation process: *basic* and *complete*. First level fields (basic, priority) are emphasized with **bold names** in the documentation. Second level fields are in *italics*.
* In addition to the documentation, please check the supporting examples and templates for clarification:

  * *example_basic.json*
  * *example_complete.json*
  * *template_basic.json*
  * *template_complete.json*


Main Blocks
===========

1. :ref:`reference`
2. :ref:`data`
3. :ref:`preprocessing`
4. :ref:`analysis_method`
5. :ref:`evaluation`
6. :ref:`result`


JSON example (main blocks)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

 {
   "reference": {
     ...
   }, 
   "data": {
     ...
   },
   "preprocessing": {
     ...
   },
   "analysis_method": {
     ...
   },
   "evaluation": {
     ...
   },
   "result": {
     ...
   }
 }

