.. _analysis_method:

Analysis Method
===============

Properties
``````````

supervised_learning
~~~~~~~~~~~~~~~~~~~

(*boolean*) It marks if a classification or regression algorithm (or any technique known as supervised learning) was used during the analysis part (e.g., a decision tree). This field specifically refers to algorithms, not methodologies or frameworks. Example:

.. code-block:: none

	"supervised_learning": true

unsupervised_learning
~~~~~~~~~~~~~~~~~~~~~

(*boolean*) It marks if a clustering algorithm (or any technique known as unsupervised learning) was used during the analysis part (e.g., DBSCAN). This field specifically refers to algorithms, not methodologies or frameworks. Example:

.. code-block:: none

	"unsupervised_learning": false

semisupervised_learning
~~~~~~~~~~~~~~~~~~~~~~~

(*boolean*) It marks if a algorithm known as semisupervised learning was used during the analysis part (e.g., Transductive SVM). This field specifically refers to algorithms, not methodologies or frameworks. Example:

.. code-block:: none

	"semisupervised_learning": true

anomaly_detection
~~~~~~~~~~~~~~~~~

(*boolean*) It marks if a algorithm known as an anomaly detection technique was used during the analysis part (e.g., LOF). This field specifically refers to algorithms, not methodologies or frameworks. Example:

.. code-block:: none

	"anomaly_detection": true

.. _tools_tag: 

.. include:: tools.rst

algorithms (*optional*)
~~~~~~~~~~~~~~~~~~~~~~~

(*array* of *objects*) *algorithms* can contain several *algorithm-objects*. An *algorithm-object* is composed of several fields: 

family
------

(*string*) The family to which the algorithm belongs. Please, consider carefully the following default labels (values):

* ``"autoregressive_models"``
* ``"bayesian"``
* ``"cluster_validation"``
* ``"crossvalidation"``
* ``"decision_tree"``
* ``"ensemble"``
* ``"entropy_based"``
* ``"fuzzy_clustering"``
* ``"glm_regression"``
* ``"graph_modeling"``
* ``"hierarchical_clustering"``
* ``"kmeans_clustering"``
* ``"kmedoids_clustering"``
* ``"knn"``
* ``"markov_process"``
* ``"mixture_model"``
* ``"neural_networks"``
* ``"parameter_search"``
* ``"pca"``
* ``"random_forest"``
* ``"rule_extraction"``
* ``"signature"``
* ``"statistics"``
* ``"stream_clustering"``
* ``"svm"``
* ``"two_step_clustering"``
* ``"wavelet_transform"``

Example:

.. code-block:: none

  "name": "fuzzy_clustering"

detail (*optional*)
-------------------

(*string*) Additional details about the algorithm name.
Example:

.. code-block:: none
  
    "subname": "Gustafson-kessel fuzzy clustering"

learning (*optional*)
---------------------

(*string*) It identifies the learning approach of the algorithm. Please, consider carefully the following default labels (values): 

* ``"supervised"``
* ``"unsupervised"``
* ``"semisupervised"``
* ``"statistics/model_fit"``
  the method uses predefined models, distributions and statistics and tries to check how real data fit such assumed models, i.e., it finds model parameters, gives summary values or discovers outliers based on distances to models. 
* ``"nest"``
  when it embeds or operates in a higher level than other nested methods. 
* ``"no"``
  it is somehow not possible to apply the word *learning* to the used algorithm        

Example:

.. code-block:: none

  "learning": "supervised"

role (*optional*)
-----------------

(*string*) This field is meaningful when diverse algorithms are compared.
Default values are:

* ``"main"``
  the method led to the best solution.
* ``"validation"``
  the algorithm is used to establish a ground truth.
* ``"competitor"``
  for all other cases.

If only one algorithm is used, it is always ``"main"``.

Example:

.. code-block:: none

  "role": "main"

type (*optional*)
-----------------

(*string*) It refers to the normal use of the defined algorithms, i.e., the algorithm is generally considered as a method for <type_value>. Please consider carefully the following default labels (values):

* ``"classification"``
The algorithm is supervised and originally intended to perform classification and class-prediction. Based on a labeled set of training data, the algorithm predicts the labels of a set of test data.
* ``"regression"``
Similar to classification, the algorithm is supervised but, instead of predicting or guessing a class/label, it outputs a predicted numerical value.
* ``"clustering"``
The algorithm is unsupervised and originally intended to find clusters within the data. Results are based on the intrinsic properties of the analyzed data and the input space drawn by such data (without resorting to any external partition or knowledge)
* ``"modeling"``
Based on a set of given assumptions and pre-knowledge, the algorithm uses some training data to create a model that summarizes a given process. The difference with other algorithm types--which might and generally do also use models--is that here the "model-according-to-some-initial-assumptions" is the focus of the process (i.e., knowledge discovery), whereas other algorithms are focused on the predicted values (i.e., problem solving), being the model a mean or secondary otuput.
* ``"outlier_detection"``
The algorithm is unsupervised and originally created to rank data points based on their outlierness properties when compared with the rest of data points in the same dataset. Clustering algorithms can be used for outlier detection, but purely outlier detection algorithms are not forced to create a cluster-like representation of the data.
* ``"space_transformation"``
The algorithm transforms the input space into an output space that simplifies subsequent analysis, improves the visualization or understanding of the data, or removes constraints.
* ``"specific_detection"``
The algorithm is specifically crafted to capture, detect, or identify a specific type of phenomenon. These algorithms are usually based on heuristics and ad-hoc steps.
* ``"validation_optimization"``
The algorithm contributes to validate or optimize the analysis process. Such algorithms validate the outcomes of other algorithms, performs the search of optimal parameters, or nest algorithms to enhance some properties.


Example:

.. code-block:: none

     "type": "clustering"

metric/decision_criteria (*optional*)
-------------------------------------

(*string*) It assesses the used metric, similarity or dissimilarity distance, also the core of the decision making criteria. Please, consider carefully the following default labels (values): 

* ``"error/fitting_function"``
* ``"euclidean"``
* ``"mutual_information"``
* ``"correlation"``
* ``"jaccard"``
* ``"mahalanobis"``
* ``"hamming"``
* ``"exact_matching"``
* ``"manhattan"``
* ``"probabilistic"``
* ``"vote"``

Example:

.. code-block:: none

     "metric/decision_criteria": "euclidean"

tools (*optional*)
------------------

(see :ref:`tools <tools_tag>`)

source (*optional*)
-------------------

(*string*) It identifies the origin of the algorithm. Please, consider carefully the following default labels (values): 

* ``"own_proposed"``
  if authors developed and present the algorithm in the paper.
* ``"own_referenced"``
  if authors developed the algorithm but presented it in a previous publication.
* ``"referenced"``
  if authors took the method from the literature or known sources. 

Example:

.. code-block:: none

     "source": "referenced"

parameters_provided (*optional*)
--------------------------------

(*boolean* or *string*) This field expresses if the required parameters for reproducing the analysis are provided. In addition to ``true`` and ``false``, ``"partially"`` is also possible when authors provide some parameters but some of them is missing or, for any reason, the experiment seems to be not reproducible. 

.. note:: If the method has no parameters, use ``true``, since you have enough information to replicate it.

Example:

.. code-block:: none

     "parameters_provided": "partially"

JSON example (analysis_method, complete)
````````````````````````````````````````

.. code-block:: none

  "analysis_method": {
    "supervised_learning": false,
    "unsupervised_learning": true,
    "semisupervised_learning": true,
    "anomaly_detection": true,
    "tools": [
        {
            "tool": "matlab_fuzzyclusteringtoolbox",
            "detail": "none",
            "availability": "public"
        },
        {
            "tool": "own_matlab_scripts",
            "detail": "none",
            "availability": "private"
        }
    ],
    "algorithms": [
        {
            "family": "fuzzy_clustering",
            "detail": "Gustafson-kessel fuzzy clustering",
            "learning": "unsupervised",
            "role": "main",
            "type": "clustering",
            "metric/decision_criteria": "mahalanobis",
            "tools": [
                {
                    "tool": "matlab_fuzzyclusteringtoolbox",
                    "detail": "none",
                    "availability": "public"
                }
            ],
            "source": "referenced",
            "parameters_provided": false
        },
        {
            "family": "statistics",
            "detail": "Mad-based outlier removal",
            "learning": "statistics/model_fit",
            "role": "main",
            "type": "outlier_detection",
            "metric_distance": "mahalanobis",
            "tools": [
                {
                    "tool": "own_matlab_scripts",
                    "detail": "none",
                    "availability": "private"
                }
            ],
            "source": "referenced",
            "parameters_provided": false
        }
    ]
  },

