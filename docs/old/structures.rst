Aggregations, Flows & Packets
=============================

* The ``packets`` directive serves the purpose of representing feature-vectors which represent packets.
* The ``flows`` directive allows representing aggregations of packets, according to a specific key.
* The ``flow-aggregations`` directive is used for representing aggregations of flows, according to a specific key.

In short, packets are to flows as flows are to aggregations.

All of these directive refer to lists of ``packet``/``flow``/``flow-aggregation`` (respectively).
This is because papers frequently try different feature vectors for different goals, and/or for comparison among them.
This way, we can keep the information of the multiple feature-vectors, without having multiple different specifications for the same paper.

Each ``packet``/``flow``/``flow-aggregation`` contains a list of features (directive ``features``), a list of free-text goals (directive ``goals``), in which you can write the problem the authors were addressing, and a free-text tool (directive ``tool``), in which you should put the tool that was used to extract the features (e.g.: tshark, yaf, etc).
The ``flow`` and ``flow-aggregation`` directives contain additionally a specification of the key used (directive ``key``), and a time window (directive ``window``), in seconds.

Key
---

The ``key`` directive contains itself some more fields:

.. include:: ../../specification.txt
    :literal:
    :start-after: # key
    :end-before: # end

The ``key_features`` directive indicates the features used for a flow/flow-aggregation.
If you do not know the features being used as key, use ``null`` or leave empty.
If there is no key (as in, everything is aggregated together), use an empty list (``[]``).

The ``bidirectional`` directive indicates whether a flow is unidirectional (only has packets with the exact same key as in ``key_features``), bidirectional (has packets with the same key as in ``key_features``, and packets in the opposite direction) or "separate_directions" (has packets as if it was bidirectional, but the features in the ``features`` directive are evaluated twice, once for each direction; i.e. if you have octetTotalCount in the features list, and key has "separate_directions",
you will get two features, one with the octetTotalCount in the packets in one direction, and another in the opposite direction).

Definition of ``bidirectional``:

.. include:: ../../specification.txt
    :literal:
    :start-after: # bidirectional
    :end-before: # end

The following is an example of the very common unidirectional 5-tuple key:

.. code-block:: none

    "key": {
      "bidirectional": false,
      "key_features": [
        "protocolIdentifier", 
        "sourceIPv4Address", 
        "sourceTransportPort", 
        "destinationIPv4Address", 
        "destinationTransportPort"
      ]
    }

Traffic Type
~~~~~~~~~~~~

The ``traffic_type`` directive is to be used when only traffic of a certain type is used.
Its definition follows:

.. include:: ../../specification.txt
    :literal:
    :start-after: # traffic_type
    :end-before: # end

Definitions
-----------

Definition of ``packet``:

.. include:: ../../specification.txt
    :literal:
    :start-after: # packets
    :end-before: # end

Definition of ``flow``:

.. include:: ../../specification.txt
    :literal:
    :start-after: # flows
    :end-before: # end

Definition of ``flow-aggregation``:

.. include:: ../../specification.txt
    :literal:
    :start-after: # flow-aggregations
    :end-before: # end
