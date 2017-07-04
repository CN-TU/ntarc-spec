Overview
========

The specification of this format is written as a grammar, in which everything are terminal symbols, except those surronded by ``<...>``.
As this is a JSON file, the spaces/newlines specified in this grammar are irrelevant.
The only thing relevant is that the final JSON file contains all the information you can gather, and that **it is JSON parseable**, with the structure defined in this document.
For details on the JSON format in general, check JSON_.

This is the high-level structure of a paper JSON file:

.. include:: ../../specification.txt
    :literal:
    :start-after: # paper
    :end-before: # end

As is usual in JSON, all fields are optional, but it is good to write as complete specification of a paper as possible.
On the other end, adding extra fields for specific papers is OK, for example for comments you want to make.

The next sections go into detail about the multiple directives introduced in the snippet above.

.. _JSON: http://www.json.org
