Workflow
========

The following should be the basic workflow:

1) look at paper
2) create json file in papers/YEAR/LNAME_1STWORD.json, with YEAR the year of the paper, LNAME the author's last name and 1STWORD the first word (or first two) of the title, all of this in lowercase; check existing files for consistency
3) run verify script and check that it agrees with what you wrote
4) add contribution to ``done_papers_list.csv``
5) commit (and push if possible) changes

.. Note:: There are papers which look like they have features on a first look, but turn out not to have any on deeper inspection.
    If this is the case, just move onto the next paper.


Verify Script
-------------

Run ``./verify PATH/TO/PAPER.json``, and verify that the output corresponds to what you expected.
This script is not a complete verification form: if it says that something is wrong, it means that something is wrong; however it is possible that something is wrong with the JSON file and the script does not complain.

The output of this script (when no errors are raised) is just a count of objects in several fields.

Common Problems
---------------

Problems with Features
~~~~~~~~~~~~~~~~~~~~~~

Cannot write the feature, because...

    * ... it is obviously too complicated to write in a structured system: just give it a name starting with `__` (double underscore), which is descriptive of what it does
    * ... I see multiple ways of doing it with the current format specification: the features specification should not be ambiguous, so if this happens either there is something wrong with the specification (very likely), or you are misunderstanding something about it; report this to Daniel and/or open a redmine ticket
    * ... I think it is possible to represent, but I am having trouble with it: use ``{"basedon": [FEATURE1, FEATURE2, ..., FEATUREN]}``, or ask for help; don't get stuck in something like this

Problems with Methods/Evaluation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cannot write a field, because...

    * ... none of the possible options fit my case: add something that makes sense. This fields are less mature, so it is likely that there are other options we haven't thought of. Do let everyone know about it though (add a redmine issue if necessary)
    * ... I don't know which to choose: ask for help, don't get stuck in something like this
