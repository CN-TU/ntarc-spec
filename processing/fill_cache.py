from analyze import *
from conf import PROJECT_PATH


PAPERS_DIR = PROJECT_PATH + '/papers'


goals = list_goals(PAPERS_DIR)
print(goals)

for pap in list_references(PAPERS_DIR):
    print(pap.title, pap.citations)
