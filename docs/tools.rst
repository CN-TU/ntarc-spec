tools
~~~~~

(*array* of *objects*) Here we describe the tools used for the preprocessing (data extraction, feature generation and transformations).

Example:

.. code-block:: none

     "tools": [
         {
             "tool": "tshark",
             "detail": "v2.0.0",
             "availability": "public"
         },
         {
             "tool": "own_python_scripts",
             "detail": "none",
             "availability": "private"
         },
         {
             "tool": "own_perl_scripts",
             "detail": "none",
             "availability": "private"
         }
     ]

tool
----
(*string*) We use the following keys for the nomenclature:
  
   a) if they are released tools, software or suites, they must be appear with the corresponding name; e.g., *tshark*, *silk*, *tcpdump*.  
   b) if they consist on scripts or plugins for well-known programming languages, suites, packages or environments, the name must reflect such dependency; e.g., *matlab_scripts*, *java_scripts*, *python_scripts*. 
   c) only the top-dependency must be shown (e.g., *matlab*). Additional *relevant* packages running under the same environment should be also added as *tools*.
   d) names start with *own_* if they are presented in the paper or referred to previous publications by the same authors (and they do not fit case 'a.'); e.g., *own_matlab_scripts*.

Example:

.. code-block:: none

  "tool": "tshark"

detail (*optional*)
-------------------

(*string*) This field expresses important details about the referred tools (e.g., version, release). If no details are required, ``"none"`` should be written in the corresponding place. Example:

.. code-block:: none
    
  	"detail": "v2.0.0"

 
availability
------------

(*strings*) This field expresses the availability of the referred tool. Please, consider carefully the following default labels (values):
   
``"public"``, ``"private"``, ``"public_on_demand"``, ``"commercial"``

Example:

.. code-block:: none
    
  	"availability": "public"
