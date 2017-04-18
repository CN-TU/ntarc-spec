.. _result:

Result
======

#. **main_goal** (*string*) This field should contain the main paper goal. In case of doubt, abstract and conclusion sections should help to establish this value. Please, consider carefully the following default labels (values):

    * ``"anomaly_detection"``
    * ``"traffic_classification"``
    * ``"botnet_detection"``
    * ``"specific_malware_detection"``
    * ``"network_properties_monitoring"``

    Example:

    .. code-block:: none

         "main_goal": "traffic_classification"

#. **subgoals** (*array* of *strings*) Here additional paper goals are collected. Goals are usually aimed in the *abstract* and must be understood as the *motivations* that inspire and justify the research. Please, repeat the main goal in this array and consider the following possible labels (values):

    ``"anomaly_detection"``, ``"traffic_classification"``, ``"botnet_detection"``, ``"specific_malware_detection"``, ``"network_properties_monitoring"``, ``"dos_detection"``, ``"ddos_detection"``, ``"user_to_root_detection"``, ``"probe_detection"``, ``"p2p_traffic_classification"``, ``"application_classification"``, ``"remote_to_local_detection"``, ``"attack_classification"``, ``"p2p_botnet_detection"``, ``"application_protocol_detection"``, ``"classification_of_encrypted_traffic"``, ``"traffic_rate_prediction"``, ``"traffic_visualization"``, ``"classification_for_qos"``, ``"http_intrusion_detection"``

    Example:
    
    .. code-block:: none
    
         "subgoals": ["traffic_classification", "dos_detection"]

#. **focus_main** (*string*) This field tries to capture the main aspect where the paper focuses the efforts. In other words, where the main novelty/proposal of the paper is located. Please, consider carefully the following default foci (values):

     * ``"algorithm"``
       authors present a new algorithm that outperforms old approaches. 
     * ``"methodology/framework"``
       the novelty is on the methodology or framework devised to properly deal with network traffic. i.e., a combination of steps, that can include: preprocessing, filtering, analysis methods, verification, etc.  
     * ``"features"``
       the main contribution of the paper is on the selected features, the preprocessing or the methods presented to select features. 
     * ``"pattern_analysis"`` 
       authors insist and describe the shape of a set of discovered patterns that represent traffic classes or attacks. 
     * ``"outlier_analysis"`` 
       authors focuses on describing discovered anomalies and offer a complete dissection of such anomalies and their peculiarities.  
     * ``"data_description"``
       the nature of the paper is mostly descriptive. Authors try to explain the Internet, network traffic or a significant part of it by exploring and depicting one or some datasets. 

   Example:

   .. code-block:: none
  
        "focus_main": "pattern_analysis"

#. **claimed_improvements** (*array* of *strings*) We specifically refer to improvements claimed in the *conclusions* section. Please, consider carefully if the claimed improvements appear in the following default list:

    * ``"improved_detection_rates"``
    * ``"improved_traffic_classification"``  
    * ``"new_phenomena_disclosed"``
    * ``"fast_processing"``
      also referred as: lightweight approach, low time-complexity, etc. 
    * ``"reduced_computational_resources"``
      in terms of memory, storage or dependencies 
    * ``"good_transportability"``
      as the capability of being integrated in diverse environments and structures, also compatibility, portability or usability.  
    * ``"enhanced_functionality"``
      being a more complete option than competitors because additional or further functions are implemented or it gathers/integrate diverse solutions together.
    * ``"improved_data_description"``
      datasets (i.e. network traffic) are more accurately described or with a higher granularity, more phenomena or characteristics, better level of detail. 
    * ``"parallelization_oriented"``
      the presented methods are designed for or ensured to be suitable for parallel computing structures.
    * ``"big_data_oriented"``
      the presented methods are claimed to be suitable for big data (aka large datasets).
    * ``"data_stream_oriented"``
      the presented methods are claimed to be suitable for data stream mining or analysis.
 
   Example:

   .. code-block:: none
  
        "claimed_improvements": ["improved_detection_rates","reduced_computational_resources"]

#. **reproducibility** (*string*) This field states if, based on the opinion of the paper data curator, the experiments and analysis can be reproduced or repeated. Please, consider carefully the following default terms (values):

    * ``"reproducible"``
      experiments are fully reproducible by a different team after reading the paper. The setup, all parameters, tools and datasets are described and/or provided (references to valid links) in a clear and open way. Results are expected to be the same or very similar.
    * ``"replicable"``
      the experiment can be replicated by a different team but with a different setup. The methodology is clearly explain, at least in a theoretical level. Not all parameters or tools are provided, but readers have enough know-how in the paper and references to develop their own setups based on the provided descriptions. Therefore, they can replicate the experiments. 
    * ``"repeteable"``
      methodologies and setups are clearly described with scientific rigor; however, experiments can only be repeated by the authors given that some resources are not publicly available (e.g., using own datasets).
    * ``"no"``
      important information about part of the methodology is missing in a way that the experiment cannot be repeated in comparable conditions. The paper show findings or results, but it is not clear how they were obtained (this information is hidden, omitted or just missing).  
 
   Example:

   .. code-block:: none
  
        "repoducibility": "replicable"


JSON example (result, complete)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

  "result": {
    "main_goal": "traffic_classification",
    "goals": ["traffic_classification"],
    "focus_main": "methodology/framework",
    "claimed_improvements": ["improved_data_description", "improved_traffic_classification", "fast_processing", "_flaw_detection"]
    "reproducibility": "replicable"
  }

