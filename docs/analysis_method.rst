.. _analysis_method:

Analysis Method
===============

1. **supervised_learning**
(boolean) It marks if a classification or regression algorithm (or any technique known as supervised learning) was used during the analysis part (e.g., a decision tree). This field specifically refers to algorithms, not methodologies or frameworks. Example:

  .. code-block:: none

	"supervised_learning": "true"

2. **unsupervised_learning**
(boolean) It marks if a clustering algorithm (or any technique known as unsupervised learning) was used during the analysis part (e.g., DBSCAN). This field specifically refers to algorithms, not methodologies or frameworks. Example:

  .. code-block:: none

	"unsupervised_learning": "false"

3. **semisupervised_learning**
(boolean) It marks if a algorithm known as semisupervised learning was used during the analysis part (e.g., Transductive SVM). This field specifically refers to algorithms, not methodologies or frameworks. Example:

  .. code-block:: none

	"semisupervised_learning": "true"

4. **anomaly_detection**
(boolean) It marks if a algorithm known as an anomaly detection technique was used during the analysis part (e.g., LOF). This field specifically refers to algorithms, not methodologies or frameworks. Example:

  .. code-block:: none

	"anomaly_detection": "true"

5. **tools**
(array of strings) Here we describe the tools used for the analysis. We use the following keys for the nomenclature: 
     
    a) if they are released tools, software or suites, they must be appear with the corresponding name; e.g., *thsark*, *silk*, *tcpdump*.  
    b) if they consist on scripts or plugins for well-known programming languages, suites, packages or environments, the name must reflect such dependency; e.g., *matlab_scripts*, *java_scripts*, *python_scripts*. 
    c) only the top-dependency must be shown (e.g., *matlab*). Additional *relevant* packages running under the same environment should be also added as *tools*.
    d) names start with *own_* if they are presented in the paper or referred to previous publications by the same authors (and they do not fit case 'a.'); e.g., *own_matlab_scripts*.
 
  Example:

  .. code-block:: none

	"tools": ["matlab_fuzzyclusteringtoolbox", "own_python_scripts"]

6. *tool_details*
(array of strings) This field is linked to the previous field (*tool*) and expresses important details about the referred tools (e.g., version, release). Details shows a one-to-one correspondence with tools and respects the array order (i.e., *tool_details[1]* is for *tool[1]*). If no details are required, *none* should be written in the corresponding place. Example:

  .. code-block:: none

	"tool_details": ["none", "none"]

7. **availability_of_tools**
(array of strings) This field is linked to the *tool* field and expresses the availability of the referred tools. Availability shows a one-to-one correspondence with tools and respects the array order (i.e., *availability_of_tools[1]* is for *tool[1]*). Please, consider carefully the following default labels (values):

    *public*, *private*, *public_on_demand*, *commercial*

  Example:

  .. code-block:: none

	"availability_of_tools": ["public", "private"]

8. *algorithms*
(array of objects) *algorithms* can contain several *algorithm-objects*. An *algorithm-object* is composed of several fields: 

  8.1. *name*
   (string) The name that identifies the algorithm main family. Example:

   .. code-block:: none
  
        "name": "fuzzy clustering"

  8.2. *subname*
   (string) A subname that can be more specific and refer to algorithm specification or subclass. Example:

   .. code-block:: none
  
        "subname": "gustafson-kessel"

  8.3. *learning*
   (string) It identifies the learning approach of the algorithm. Please, consider carefully the following default labels (values): 

      * *supervised*
      * *unsupervised* 
      * *semisupervised* 
      * *statistics/model_fit*
         the method uses predefined models, distributions and statistics and tries to check how real data fit such assumed models, i.e., it finds model parameters, gives summary values or discovers outliers based on distances to models. 
      * *nest*
         when it embeds or operates in a higher level than other nested methods. 
      * *no*
         it is somehow not possible to apply the word *learning* to the used algorithm        

   Example:

   .. code-block:: none
  
        "learning": "supervised"

  8.4. *role*
   (string) This field is meaningful when diverse algorithms are compared. Default values are: *main*, when the method led to the best solutions; and *competitor* for other cases. If only one algorithm is used, it is always *main*. If the algorithm is used to establish a ground truth, its *role* is *validation*. Example:

   .. code-block:: none
  
        "role": "main"

  8.5. *type*
   (string) It identifies the type of algorithm with regard to analysis main approaches. Please, consider carefully the following default labels (values): 

      * *classification*
      * *regression*
      * *clustering*
      * *anomaly_detection*
      * *heuristics*
        the algorithm is quite ad-hoc and based on rules and equations defined by the authors' expert knowledge.
      * *statistics*
        the algorithm belongs to the statistics domain and uses parametric or non-parametric models to explain the data.
      * *text_matching*
        the algorithm bases its classification and decisions on searching for specific text strings or comparing text strings.

   Example:

   .. code-block:: none
  
        "type": "heuristics"

  8.6. *metric/decision_criteria*
   (string) It assesses the used metric, similarity or dissimilarity distance, also the core of the decision making criteria. Please, consider carefully the following default labels (values): 

      * *error/fitting_function*
      * *euclidean* 
      * *mutual_information*
      * *correlation*
      * *jaccard*
      * *mahalanobis*
      * *hamming*
      * *exact_matching*
      * *manhattan* 
      * *probabilistic*
      * *vote*

   Example:

   .. code-block:: none
  
        "metric/decision_criteria": "euclidean"

  8.7. *tool*
   Like in 5 but (string).

  8.8. *tool_detail*
   Like in 6 but (string).

  8.9. *availability_of_tool*
   Like in 7 but (string).

  8.10. *source*
   (string) It identifies the origin of the algorithm. Please, consider carefully the following default labels (values): 

      * *own_proposed*
        if authors developed and present the algorithm in the paper.
      * *own_referenced*
        if authors developed the algorithm but presented it in a previous publication.
      * *referenced*
        if authors took the method from the literature or known sources. 
 
   Example:

   .. code-block:: none
  
        "source": "referenced"

  8.11. *parameters_provided*
   (almost-boolean) This field expresses if the required parameters for reproducing the analysis are provided. In addition to *true* and *false*, *partially* is also possible when authors provide some parameters but some of them is missing or, for any reason, the experiment seems to be not reproducible. 

   Example:

   .. code-block:: none
  
        "parameters_provided": "partially"



JSON example (analysis_method, complete)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

  "analysis_method": {
    "supervised_learning": "false",
    "unsupervised_learning": "true",
    "semisupervised_learning": "true",
    "anomaly_detection": "true",
    "tools": ["matlab_fuzzyclusteringtoolbox", "own_matlab_scripts"],
    "tool_details": ["none", "none"],
    "availability_of_tools": ["public", "private"],
    "algorithms": [
        {
            "name": "fuzzy clustering",
            "subname": "gustafson-kessel",
            "learning": "unsupervised",
            "role": "main",
            "type": "clustering",
            "metric/decision_criteria": "mahalanobis",
            "tool": "matlab_fuzzyclusteringtoolbox",
            "tool_detail": "none",  
            "availability_of_tool": "public",
            "source": "referenced",
            "parameters_provided": "false"
        },
        {
            "name": "mad-based outlier removal",
            "subname": "double mad",
            "learning": "statistics/model_fit",
            "role": "main",
            "type": "anomaly_detection",
            "metric_distance": "mahalanobis",
            "tool": "own_matlab_scripts", 
            "tool_detail": "none",  
            "availability_of_tool": "private",
            "source": "referenced",
            "parameters_provided": "false"
        }
    ]
  },

