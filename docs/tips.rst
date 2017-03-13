Tips
====


* GROUND TRUTH FOR EVALUATION -- FIV, Mar 13, 2017

I guess you might have noticed that many flow-based analysis validate/evaluate/verify their results by comparing their methods with other techniques (usually payload-based) that work as benchmarks. This is important for evaluations because, obviously, results (performance scores) are strongly linked to the benchmark (e.g., a classifier that obtains 100% of accuracy differentiating trivial classes like "TCP", "UDP", "ICMP" and "other-protocols" is not a breakthrough even though the nice classification performance). To collect related info I'm adding two fields in the <evaluation> group. They are:

.. code-block:: none

	"ground_truth": "packet_inspection" | "manual_verification" | "labeled_data" | "method_comparison"
	"ground_truth_tool": {the specific name of the tool/method} 

* FEATURE SELECTION, X-VALIDATION,... NESTED METHODS -- FIV, Mar 10, 2017

In some papers authors carry out "feature selection" and/or "cross-validation" as part of the analysis methods. They do not completely fit our templates, but it is very important to collect such information because these are two good examples of steps commonly considered as "good practices" (if not necessary) and, in many cases, not performed.

It does not make sense saying if X-validation is "supervised" or "unsupervised". Well, you could argue both definitions, because it is not supervised by itself but actually embeds/nests a supervised method.

Therefore, I would propose, at some point, to use perhaps <learning> instead of the <supervision> field (in order not to make things more complicated, leave it like it is right now; I guess we can change it in the future automatically with some parsing tool). Anyway, the options would be:

.. code-block:: none
	<learning> (current <supervision>):
   		-"supervised"
   		-"unsupervised"
  		-"semi_supervised"
   		-"descriptive"
   		-"nest"

"descriptive" is for analysis methods that just give some plain description or summary of the analyzed data. Some examples of "nest" methods would be: stability selection, forward or backward selection (regression), consensus clustering, cross-validation, ensemble learning, etc.

I would also include "feature_selection" as a new method <type>. It will be relevant to easily search which papers used feature selection in their methods.

* UNIDIRECTIONAL FEATURES IN BIDIRECTIONAL FLOWS -- FIV, Mar 8, 2017

You might find features that are unidirectional for flows defined bidirectionals. For example, given the flow A<>B, authors can use the total number of bytes from: (1) A to B, (2) B to A, or (3) both. In such cases, remember to define the <bidirectional> attribute as "separate_directions". Also, you can create the "_client_to_server" and "_server_to_client" faetures to discriminate the A>B and A<B situations (see the example below).

.. code-block:: none

	"features": [
		{"basedon": ["octetTotalCount","_server_to_client"]},
		{"basedon": ["octetTotalCount","_client_to_server"]},
		"octetTotalCount",
	], 


* BAYES CLASSIFIER (SIMILARITY METRIC) -- FIV, Mar 8, 2017

If you wonder which <similarity_metric> is used by bayes classifiers, they don't use any, they are probabilistic classifiers, so, in our case, we can just write "other", or alternatively, "probabilistic".


* PAPERS WITH MANY FEATURES -- FIV, Mar 8, 2017
 
If you find a paper which uses many features or a high dimensional feature space (e.g. Tstat), they will probably perform kinda feature selection. Therefore, focus on the "meaningful" set of features for the extracted info (usually below 10 or 20). If not, just switch to a different paper and place this one in a low-priority list.


* FEATURE SELECTION METHODS -- FIV, Mar 8, 2017

In case of feature selection "methods". If you see:

<whatever> filter --> they are usually "unsupervised" methods.

<whatever> wrapper (e.g., stepwise regression, forward selection, backward elimination) --> they are usually "supervised" and embed a classifier (type: "regression" and you add another entry for the classifier).

<whatever> hybrid --> they are mixed (we could also say "semi-supervised")

If authors are really good, they will use "stability selection" (everybody should do this ;) ). Stability selection is kinda bootstrapping and nests/embeds a feature selection method. Therefore...

.. code-block:: none

	{
		"name": "Stability selection",
		"supervision": "unsupervised",
		"type": "statistics",
		"similarity_metric": "euclidean"(1)
	}

(1): Or "other", or null. Well, it just weights performance indices...

