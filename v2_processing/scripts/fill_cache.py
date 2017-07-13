from utils.analyze import *
from conf import PROJECT_PATH


PAPERS_DIR = PROJECT_PATH + '/data/v2_papers'


goals = list_goals(PAPERS_DIR)
print(goals)

for pap in list_references(PAPERS_DIR):
    print(pap.title, pap.citations)
    for affil in pap._affiliations:
        print(affil.name, affil.location)
