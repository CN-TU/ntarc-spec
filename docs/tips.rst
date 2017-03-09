Tips
====


* UNIDIRECTIONAL FEATURES IN BIDIRECTIONAL FLOWS -- FIV, Mar 8, 2017

You might find features that are unidirectional for flows defined bidirectionals. For example, given the flow A<>B, authors can use the total number of bytes from: (1) A to B, (2) B to A, or (3) both. In such cases, remember to define the <bidirectional> attribute as "separate_directions". Also, you can create the "_client_to_server" and "_server_to_client" faetures to discriminate the A>B and A<B situations (see the example below).

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

-<whatever> filter --> they are usually "unsupervised" methods
-<whatever> wrapper (e.g., stepwise regression, forward selection, backward elimination) --> they are usually "supervised" and embed a classifier (type: "regression" and you add another entry for the classifier)
-<whatever> hybrid --> they are mixed (we could also say "semi-supervised")

If they are really good, they will use "stability selection" (everybody should do this ;) ). Stability selection is kinda bootstrapping and nest/embed a feature selection method. Therefore...

      {
          "name": "Stability selection",
          "supervision": "unsupervised",
          "type": "statistics",
          "similarity_metric": "euclidean"(1)
      }

(1): Or "other", or null. Well, it just weights performance indices...

