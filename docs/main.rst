

Main Blocks
===========

The main blocks are ordered according to the typical processing pipeline:::

    Data > Preprocessing > Analysis Method > Evaluation > Result


The **Reference** block contains information about the publication itself (title, authors, etc) and the curator of the paper.

The **Data** block contains information about the datasets used in the publication.

The **Preprocessing** block contains information about the processing done to the data before passing it on to an analysis method.
This process usually consists of extracting vectors of features from the original data.

The **Analysis Method** block contains information about what analytical methods were used in the publication.

The **Evaluation** block contains in information about how the performance of the methods in the previous section was evaluated.

The **Result** block contains information about the conclusions of the paper.
The information for this block is usually completely contained in the conclusion section of the paper.

Additionally to the main blocks, in order to avoid confusion with past/future versions of the format, there is a mandatory field for version (which is always "v2").


JSON example
~~~~~~~~~~~~

Summary with only the main blocks:

.. code-block:: none

 {
   "version": "v2",
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

Example of a complete file:

.. include:: ../example_complete.json
   :literal:
