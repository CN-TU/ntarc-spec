Features
========

The features are the hardest part of this format, as they are the most complex.
However, having a complete description of the feature-set used in a paper in this format allows the use of an extractor tool to automatically reproduce the feature vectors used in the paper.

Concepts
--------

* Features
    A feature represents a value which can be extracted from a packet/flow/flow aggregation.
    These can be base features (often can be computed by looking only at packet headers), or some more complicated things (like the entropy of a value that can be found in the packet headers).
    In our format, each feature is a combination of operations applied to base features.
    Each feature must be only one scalar value (as opposed to a vector).
* Base features
    Base features are the basic elements of our features format.
    These are always represented by strings.

    Examples: ``"packetTotalCount"``, ``"octetTotalCount"``, ``"sourceIPv4Address"``
* Operations
    We have multiple operations defined, which receive features as arguments.
    These are defined as a JSON dictionary with one key, in which the key is the name of the operation, and the corresponding value is a list of arguments.

    Examples: ``"mean"``, ``"add"``, ``"log"``
* Selections
    We also have an option to filter out specific packets in a flow/flow aggregation.
    This allows us for example to count the number of packets with a specific property (e.g., packet size larger than some threshold).

Base Features
-------------

We call base features those which are not obtained by combining other features.
These are represented in this format by JSON strings.

We try to use the names of the IPFIX information elements defined by `IANA <http://www.iana.org/assignments/ipfix/ipfix.xhtml#ipfix-information-elements>`_.
For features that we can not get out of combining IANA features with our limited set of operations, we have two naming options:

    * if the feature is expected to be used many times (e.g.: there are some KDD '99 features which we cannot represent using IANA features and operations, but they are used in many papers), use a ``_`` as prefix to a descriptive feature name.
      This features are listed in :download:`own_ies.csv <../own_ies.csv>`.
      If you want to specify a new ``_`` feature, you need to add it there.
    * if the feature is very specific to this paper, use ``__`` (double ``_``) as prefix to a descriptive feature name

In both of this cases, try to give descriptive feature names, similar to the the ones used by IANA.

This means that **all base features that do not start with** ``_`` **have to be IPFIX information elements defined by IANA**.

There is still another case, which is features that are repeated often, and are a combination of IANA features.
In this case, use a descriptive feature name which starts with ``_`` as an alias for it.
A complete list of aliases is in :download:`feature_aliases.json <../feature_aliases.json>`; please add additional aliases there.


Operations
----------

Besides the base features, we also have some ``operations``, by which we can get new features.

We can have two kinds of operations:

* value
    The output is a single scalar value.
* values
    The output is a vector of values (possibly of variable size).

.. note:: The highest level operation in a feature **cannot** be one that is defined in the ``<values>`` directive, as that outputs multiple values.

Below is a grammar defining the list of possible operations, and their respective arguments:

Value:

.. include:: ../specification.txt
    :literal:
    :start-after: # operation
    :end-before: # end

Values:

.. include:: ../specification.txt
    :literal:
    :start-after: # values
    :end-before: # end


Selections
----------

The ``selection`` directive is useful for filtering out packets or any other information which might not be interesting for a particular feature.
Intuitively, using selection on a flow will select packets (that is, the result will be the packets that fulfill the conditions in the selection), and in a flow_aggregation will output either flows or packets, depending on the selection used.
Because of this distinction, for each selection that outputs packets, there is another selection that outputs flows, and contains ``"_flows"`` in its name.

This distinction between outputting flows or packets is necessary, since you can select objects with ``"octetTotalCount"`` > 1000, and in this case it's ambiguous whether you want to select all packets with more than 1000 bytes, or all the flows with more than 1000 bytes.
Note that some features only make sense for flows (e.g., ``"packetTotalCount"``).

Its syntax is the following:

.. include:: ../specification.txt
    :literal:
    :start-after: # selection
    :end-before: # end

The ``logic`` directive contains the test to decide what gets or not filtered.
Definition of ``logic``:

.. include:: ../specification.txt
    :literal:
    :start-after: # logic
    :end-before: # end

Example Features
----------------

The following are examples of the ``features`` directive.

.. code-block:: none

      "features": [
        "protocolIdentifier",
        "sourceTransportPort",
        "destinationTransportPort",
        "octetTotalCount",
        "packetTotalCount",
        "_activeForSeconds",
        {"divide": ["octetTotalCount", "_activeForSeconds"]},
        {"divide": ["packetTotalCount", "_activeForSeconds"]},
        "__maximumConsecutiveSeconds",
        "__minimumConsecutiveSeconds",
        {"maximum": ["_interPacketTimeMicroseconds"]},
        {"minimum": ["_interPacketTimeMicroseconds"]},
        {"count": [{"select": [{"geq": ["_interPacketTimeMicroseconds", 1000000]}]}]}
      ]


.. code-block:: none

        "features": [
          {"entropy": ["sourceIPv4Address"]}, 
          {"entropy": ["destinationIPv4Address"]}, 
          {"entropy": ["destinationTransportPort"]}, 
          {"entropy": ["_flowDurationSeconds"]}, 
          {"multiply": [{"argmax": [{"count": [{"select": [{"less": ["ipTotalLength", 128]}]}]}, {"count": [{"and": [{"select": [{"geq": ["ipTotalLength", 128]}]}, {"select": [{"less": ["ipTotalLength", 256]}]}]}]}, {"count": [{"and": [{"select": [{"geq": ["ipTotalLength", 256]}]}, {"select": [{"less": ["ipTotalLength", 512]}]}]}]}, {"count": [{"and": [{"select": [{"geq": ["ipTotalLength", 512]}]}, {"select": [{"less": ["ipTotalLength", 1024]}]}]}]}, {"count": [{"and": [{"select": [{"geq": ["ipTotalLength", 1024]}]}, {"select": [{"less": ["ipTotalLength", 1500]}]}]}]}]}, {"add": [{"entropy": [{"count": [{"select": [{"less": ["ipTotalLength", 128]}]}]}]}, {"entropy": [{"count": [{"and": [{"select": [{"geq": ["ipTotalLength", 128]}]}, {"select": [{"less": ["ipTotalLength", 256]}]}]}]}]}, {"entropy": [{"count": [{"and": [{"select": [{"geq": ["ipTotalLength", 256]}]}, {"select": [{"less": ["ipTotalLength", 512]}]}]}]}]}, {"entropy": [{"count": [{"and": [{"select": [{"geq": ["ipTotalLength", 512]}]}, {"select": [{"less": ["ipTotalLength", 1024]}]}]}]}]}, {"entropy": [{"count": [{"and": [{"select": [{"geq": ["ipTotalLength", 1024]}]}, {"select": [{"less": ["ipTotalLength", 1500]}]}]}]}]}]}]}, 
          {"get": [14, "tcpControlBits"]}
        ]


.. code-block:: none

	"features": ["_KDD5", "_KDD23", "_KDD3", "_KDD6", "_KDD35", "_KDD1"]
