import csv
from parse import *
from conf import PROJECT_PATH


PAPERS_DIR = PROJECT_PATH + '/papers'


methods = method_name_to_all(PAPERS_DIR)

with open(PROJECT_PATH + '/methods.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['Name', 'Count', 'supervision', 'type', 'similarity_metric', 'papers'])
    for method, vals in iter(sorted(methods.items())):
        writer.writerow([method,
                         vals['count'],
                         list(vals['supervision']),
                         list(vals['type']),
                         list(vals['similarity_metric']),
                         vals['papers']])

supervision = method_supervision_count(PAPERS_DIR)

with open(PROJECT_PATH + '/methods_supervision.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['supervision', 'count'])
    for sup, count in supervision.items():
        writer.writerow([sup, count])


method_type = method_type_count(PAPERS_DIR)

with open(PROJECT_PATH + '/methods_type.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['type', 'count'])
    for t, count in method_type.items():
        writer.writerow([t, count])


similarity_metric = method_similarity_metric_count(PAPERS_DIR)

with open(PROJECT_PATH + '/methods_similarity_metric.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['similarity_metric', 'count'])
    for sim, count in similarity_metric.items():
        writer.writerow([sim, count])
