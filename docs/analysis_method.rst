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

name
----

(*string*) The name that identifies the algorithm main family. Example:

.. code-block:: none

  "name": "fuzzy clustering"

subname (*optional*)
--------------------

(*string*) A subname that can be more specific and refer to algorithm specification or subclass. Example:

.. code-block:: none
  
    "subname": "gustafson-kessel"

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

(*string*) It identifies the type of algorithm with regard to analysis main approaches. Please, consider carefully the following default labels (values): 

* ``"classification"``
* ``"regression"``
* ``"clustering"``
* ``"anomaly_detection"``
* ``"heuristics"``
  the algorithm is quite ad-hoc and based on rules and equations defined by the authors' expert knowledge.
* ``"statistics"``
  the algorithm belongs to the statistics domain and uses parametric or non-parametric models to explain the data.
* ``"text_matching"``
  the algorithm bases its classification and decisions on searching for specific text strings or comparing text strings.

Example:

.. code-block:: none

     "type": "heuristics"

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
            "name": "fuzzy clustering",
            "subname": "gustafson-kessel",
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
            "name": "mad-based outlier removal",
            "subname": "double mad",
            "learning": "statistics/model_fit",
            "role": "main",
            "type": "anomaly_detection",
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

