Features
========

The features are obviously the most important part of this format, and also the most complex.

Base Features
-------------

We call base features those which are not obtained by combining other features.
These are represented in this format by JSON strings.

We try to use the names of the IPFIX information elements defined by `IANA <http://www.iana.org/assignments/ipfix/ipfix.xhtml#ipfix-information-elements>`_.
Additionally to the names defined by IANA, we also have some ``operations``, by which we can get new features.
For features that we can not get out of combining IANA features with our limited set of operations, we have two naming options:

    * if the feature is expected to be used many times (e.g.: there are some KDD '99 features which we cannot represent using IANA features and operations, but they are used in many papers), use a ``_`` as prefix to a descriptive feature name
    * if the feature is very specific to this paper, use ``__`` (double ``_``) as prefix to a descriptive feature name

In both of this cases, try to give descriptive feature names, similar to the the ones used by IANA.

This means that **all base features that do not start with** ``_`` **have to be IPFIX information elements defined by IANA**.

There is still another case, which is features that are repeated often, and are a combination of IANA features.
In this case, use a descriptive feature name which starts with ``_`` as an alias for it.
A complete list of aliases is in :file:`../dict.json`; please add additional aliases there.


Operations
----------

Below is a complete list of possible operations:

.. include:: ../specification.txt
    :literal:
    :start-after: # operation
    :end-before: # end

Value & Values
~~~~~~~~~~~~~~

The ``value`` directive represents a single value, while the ``values`` directive represents a list of values.
This is necessary to distinguish the arguments to the operations.


Selection & Logic
~~~~~~~~~~~~~~~~~

The ``selection`` directive is useful for filtering out packets or any other information which might not be interesting for a particular feature.
Intuitively, using selection on a flow will select packets (that is, the result will be the packets that fulfill the conditions in the selection), and in a flow_aggregation will select flows.

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

For this to be useful, you also need to understand the ``compare-packet`` and ``compare-flow`` directive.
In fact, they are both the same, with the only difference being that ``compare-packet`` can only refer to packet-level features, and ``compare-flow`` can only refer to flow-level features.

Definition of ``compare-packet`` and ``compare-flow``:

.. include:: ../specification.txt
    :literal:
    :start-after: # compare
    :end-before: # end

Feature Specification
---------------------

The following is the specification for the ``features`` and ``feature`` directives:

.. include:: ../specification.txt
    :literal:
    :start-after: # features
    :end-before: # end

The ``packet-feature``, ``flow-feature`` and ``aggregation-feature`` are packet, flow and aggregation -level features (respectively), which are not compositions of other features/operations.
That is, they should be strings from the IANA IPFIX information elements list, or strings that start with ``_`` or ``__``.

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
