Tips
====


* Naïve Bayes/Bayesian Networks/etc: If you wonder which <similarity_metric> is used by bayes classifiers, they don't use any, they are probabilistic classifiers, so, in our case, we can just write "other", or alternatively, "probabilistic". 

* Many features: If you find a paper which uses many features or a high dimensional feature space (e.g. Tstat), they will probably perform kinda feature selection. Therefore, focus on the "meaningful" set of features for the extracted info (usually below 10 or 20). If not, just switch to a different paper and place this one in a low-priority list. 

* Methods keywords: If you see:

  - <whatever> filter --> they are usually "unsupervised" methods
  - <whatever> wrapper (e.g., stepwise regression, forward selection, backward elimination) --> they are usually "supervised" and embed a classifier (type: "regression" and you add another entry for the classifier)
  - <whatever> hybrid --> they are mixed (we could also say "semi-supervised") 
