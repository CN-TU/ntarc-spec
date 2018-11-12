Versions
========

Old Versions
------------

Currently there are 2 simultaneous major versions, v1 and the current version.
No more work should be done for the v1 version, and it should be deleted when all the curated papers have been converted to the current version.
However, until then some useful information might be extracted from the existing v1 papers.

Versioning System
-----------------

From v2 onwards, we use `semantic versioning <https://semver.org>`_.
Papers follow the ``vMAJOR.MINOR.PATCH`` versioning.
For example, a valid version for a paper is ``v2.1.1``.
However external tools should only need to look at the ``MAJOR.MINOR`` version, and the patch number should not be fundamental to their behavior.

An increase in the MAJOR version reveals a complete change of the NTARC format.
An increate in the MINOR version indicates some small changes in the NTARC specification, that break backwards compatibility.
An increase in the PATCH version occurs every time something is changed in the specification, that doesn't break backwards compatibility.
Increases in the PATCH version should be frequent, and should happen when someone adds a new feature to our list of Information Elements, or when a new value is added to the list of previously allowed values for any specific field.

There is an exception to these rules for versions ``v2`` and ``v2.1``, since they were introduced before the decision to follow the semantic versioning system.
Some discussion on this topic can be found at https://github.com/CN-TU/nta-meta-analysis-specification/issues/14.

To summarize, we have:

* One branch for each minor version, named ``rMAJOR.MINOR`` (e.g., ``r2.1``)
* Starting from v2.1.1, we use semantic versioning
* Each change that doesn't break backwards compatibility increments the PATCH number of the version (e.g., adding possible values to fields with finite possible values; adding new IEs to ``own_ies.csv``)
* This version is included in the NTARC ``version`` field
* External tools usually only need to care about MINOR version, as everything should be backwards compatible (in particular, this should be true for the verifier)
* Tags with PATCH should be very frequent; they should be used for individual commits, or for multiple commits in a short time
* The r2 branch (corresponding to v2.0.X) is exempt from the proposed branch naming scheme, to keep compatibility with existing tools
