.. _evaluation:

Evaluation
==========

#. **algorithm_comparison** (*boolean*) It marks if different algorithms are compared in the paper in an attempt to establish the best one to fulfill a specific goal. Example:

   .. code-block:: none
 
 	"algorithm_comparison": false

#. **internal_validation** (*boolean*) It marks if algorithms were evaluated by means of internal validation methods, i.e., scores are provided based on the intrinsic properties of data under analysis (e.g., Silhouette).  Example:

   .. code-block:: none
 
 	"internal_validation": false

#. **external_validation** (*boolean*) It marks if algorithms were evaluated by means of external validation methods, e.g., baseline partitions, ground truth, pre-labeled data, dpi-classes. Example:

   .. code-block:: none
 
 	"internal_validation": false

#. **dpi-based_validation** (*boolean*) It marks if algorithms were evaluated by using the results from deep packet inspection (dpi) as benchmark. Example:

   .. code-block:: none

	"dpi-based_validation": true

#. **port-based_validation** (*boolean*) It marks if algorithms were evaluated by using the results from port-based identification (typically TCP and UDP destination ports) as benchmark. Example:

   .. code-block:: none

	"port-based_validation": false

#. **pre-knowledge-based_validation** (*boolean*) It marks if algorithms were evaluated by using some kind of pre-knowledge as benchmark. Such pre-knowledge usually means that authors prepared the data previous to the analysis according to predefined classes (e.g., ``"synthetic"`` or ``"altered_captured"``) Example:

   .. code-block:: none

	"pre-knowledge-based_validation": true

#. **manual_verification** (*boolean*) It marks if results (e.g., outliers, classes, patterns) obtained by algorithms were manually/visually checked after the analysis to see/discover if results represent specific phenomena/events. Example:

   .. code-block:: none

	"manual_verification": true

#. **implementation_in_real_scenario** (*boolean*) It marks if authors mentioned/explained/tried an actual implementation of the proposed methodology/framework/algorithms in a real scenario. If the proposed system is running in a real environment and derived experiences are documented in the paper. Example:

   .. code-block:: none

	"implementation_in_real_scenario": false

#. **train_test_separation** (*boolean*) It marks if datasets were clearly separated in independent train and test sets for the analysis. In other words, ``true`` if none of the testing data was used in training, ``false`` otherwise. Example:

   .. code-block:: none

	"manual_verification": true


#. *methods* (*array* of *objects*) *methods* can contain several *method-objects*. A *method-object* represents a technique used for the analysis evaluation or algorithm validation. A *method-object* is composed of several fields: 

   #. **name** (*string*) The name that identifies the evaluation method. Example:

      .. code-block:: none
     
           "name": "normal classification metrics"

   #. *type* (*string*) It identifies the type of evaluation method. Please, consider carefully the following default labels (values): 

      * ``"external"``
      * ``"internal"``
      * ``"external_and_internal"``
      * ``"nest"``
 
      Example:

      .. code-block:: none
  
           "type": "external"

   #. *metrics* (*array* of *string*) It assesses the used metrics for the evaluation. Please, consider carefully the following default labels (values): 

      * ``"error_distance"``
      * ``"function_fitting"``
      * ``"precision"``
      * ``"accuracy"``
      * ``"recall"``
      * ``"f-1"``
      * ``"ROC/UAC"``
      * ``"complete_confusion_matrix"``
        all information regarding the confusion matrix is provided.
      * ``"incomplete_confusion_matrix"``
        some information regarding the confusion matrix is missing and it is relevant for evaluating the quality of the classifier.
      * ``"classification_loss"``
      * ``"clustering_metrics"``
      * ``"time-based"``
      * ``"computing_resources-based"``
      * ``"granularity-based"``
        e.g., an algorithm provides more detailed information (classes, traffic types) than other algorithm.
      * ``"heuristic"``
      * ``"vote"``
        for nest methods (usually). The nest method integrates diverse validation techniques and the best result/algorithm is decided by means of consensus. 

      Example:

      .. code-block:: none
  
           "metric/decision_criteria": "euclidean"

   #. *source* (*string*) It identifies the origin of the method. Please, consider carefully the following default labels (values): 

      * ``"own_proposed"``
        if authors developed and present the algorithm in the paper.
      * ``"own_referenced"``
        if authors developed the algorithm but presented it in a previous publication.
      * ``"referenced"``
        if authors took the method from the literature or known sources. 
      * ``"popular"``
        the method is popular enough to not require a reference (e.g., FP, FN). 

      Example:

      .. code-block:: none
  
           "source": "referenced"


JSON example (evaluation, complete)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

  "evaluation": {
    "algorithm_comparison": false,
    "internal_validation": true,
    "external_validation": true,
    "dpi-based_validation": false,
    "port-based_validation": false,
    "pre-knowledge-based_validation": false,
    "manual_verification": true,
    "implementation_in_real_scenario": false,
    "train-test_separation": false,
    "methods": [
        {
            "name": "manual verification",
            "type": "external",
            "metric": "heuristics",
            "source": "popular"
        },
        {
            "name": "weighted vote",
            "type": "nest",
            "metric": "vote",
            "source": "popular"
        },
        {
            "name": "classification entropy",
            "type": "internal",
            "metric_distance": "clustering_metrics",
            "source": "referenced"
        },
        {
            "name": "partition index",
            "type": "internal",
            "metric": "clustering_metrics",
            "source": "referenced"
        },
        {
            "name": "xie and benix index",
            "type": "internal",
            "metric": "clustering_metrics",
            "source": "referenced"
        },
        {
            "name": "clustering gain",
            "type": "internal",
            "metric": "clustering_metrics",
            "source": "referenced"
        },
        {
            "name": "own cluster validity",
            "type": "internal",
            "metric": "clustering_metrics",
            "source": "missing"
        }
    ]
  }


