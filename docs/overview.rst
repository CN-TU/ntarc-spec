Overview
========

The specification of this format is written as a grammar, in which everything are terminal symbols, except those surronded by ``<...>``.
As this is a JSON file, the spaces/newlines specified in this grammar are irrelevant.
The only thing relevant is that the final JSON file contains all the information you can gather, and that **it is JSON parseable**, with the structure defined in this document.
For details of the JSON format, check JSON_.

This is the high-level structure of a paper JSON file:

.. include:: ../specification.txt
    :literal:
    :start-after: # paper
    :end-before: # end

As is usual in JSON, all fields are optional, but it is good to write as complete specification of a paper as possible.

.. _JSON: http://www.json.org
