Workflow
========

The following should be the basic workflow:

1) look at paper
2) write JSON file
3) run verify script and check that it agrees with what you wrote
4) add contribution to ``done_papers_list.csv``
5) commit (and push if possible) changes


Common Problems
---------------

Problems with Features
~~~~~~~~~~~~~~~~~~~~~~

Cannot write the feature, because...

    * ... it is obviously too complicated to write in a structured system: just give it a name starting with `__` (double underscore), which is descriptive of what it does
    * ... I see multiple ways of doing it with the current format specification: the features specification should not be ambiguous, so if this happens either there is something wrong with the specification (very likely), or you are misunderstanding something about it; report this to Daniel and/or open a redmine ticket
    * ... I think it is possible to represent, but I am having trouble with it: ask for help, don't get stuck in something like this

Problems with Methods/Evaluation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cannot write a field, because...

    * ... none of the possible options fit my case: add something that makes sense. This fields are less mature, so it is likely that there are other options we haven't thought of. Do let everyone know about it though (add a redmine issue if necessary)
    * ... I don't know which to choose: ask for help, don't get stuck in something like this
