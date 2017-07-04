Repository Organization
=======================

At the moment there are 2 versions of the format, v1 and v2.
We are in the process of converting all the v1 files into v2 of our format.
This documentation includes the content for both versions, and the repository itself also supports both formats at the moment.
However, when we have converted all the files to v2, the v1 files will be removed from the repository and documentation.

This is the current structure of the repository:

.. code-block:: none

	.
	├── data                        # stores input of data curators
	│   ├── datasets.json           # v1 datasets
	│   ├── feature_aliases.json    # aliases of common features (start with '_')
	│   ├── iana_ies.csv            # complete list of IANA Information Elements
	│   ├── own_ies.csv             # list of custom Information Elements
	│   ├── papers                  # v1 papers
	│   │   └── ...
	│   ├── tools.json              # v1 tools
	│   └── v2_papers               # v2 papers
	│       └── ...
	├── datasets_specification.txt  # specification of the format for data/datasets.json
	├── docs                        # documentation of the project
	│   └── ...
	├── example_basic.json          # example for v2 (basic)
	├── example_complete.json       # example for v2 (complete)
	├── processing                  # processing tools for v1
	│   └── ... 
	├── schema_v2.json              # JSON schema for v2
	├── specification.txt           # specification for features (and for v1)
	├── tools_specification.txt     # specification of the format for data/tools.json
	├── v2_processing               # processing tools for v2
	│   └── ...
	└── verify.sh                   # verification script for v2
