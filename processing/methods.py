import csv
from parse import *
from conf import PROJECT_PATH


PAPERS_DIR = PROJECT_PATH + '/papers'
OUTPUT_DIR = PROJECT_PATH + '/csvs'


methods = method_name_to_all(PAPERS_DIR)

with open(OUTPUT_DIR + '/methods.csv', 'w') as fd:
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

with open(OUTPUT_DIR + '/methods_supervision.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['supervision', 'count'])
    for sup, count in supervision.items():
        writer.writerow([sup, count])


method_type = method_type_count(PAPERS_DIR)

with open(OUTPUT_DIR + '/methods_type.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['type', 'count'])
    for t, count in method_type.items():
        writer.writerow([t, count])


similarity_metric = method_similarity_metric_count(PAPERS_DIR)

with open(OUTPUT_DIR + '/methods_similarity_metric.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['similarity_metric', 'count'])
    for sim, count in similarity_metric.items():
        writer.writerow([sim, count])


method_one_feature_selection = method_one_feature_selection_count(PAPERS_DIR)

with open(OUTPUT_DIR + '/methods_one_feature_selection.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['at_least_one_feature_selection_method', 'count'])
    for ans, count in method_one_feature_selection.items():
        writer.writerow([ans, count])


evaluation_metrics = evaluation_metrics_count(PAPERS_DIR)

with open(OUTPUT_DIR + '/evaluation_metrics.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['evaluation metric', 'count'])
    for ev, count in evaluation_metrics.items():
        writer.writerow([ev, count])


evaluation_method_evaluation = evaluation_method_evaluation_count(PAPERS_DIR)

with open(OUTPUT_DIR + '/method_evaluation.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['method_evaluation', 'count'])
    for ev, count in evaluation_method_evaluation.items():
        writer.writerow([ev, count])


dataset_availability = dataset_availability_count(PAPERS_DIR)

with open(OUTPUT_DIR + '/dataset_availabilities.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['dataset_availability', 'count'])
    for av, count in dataset_availability.items():
        writer.writerow([av, count])


dataset_one_public = dataset_one_public_count(PAPERS_DIR)

with open(OUTPUT_DIR + '/dataset_one_public.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['at_least_one_public', 'count'])
    for av, count in dataset_one_public.items():
        writer.writerow([av, count])


dataset_type = dataset_traffic_type(PAPERS_DIR)

with open(OUTPUT_DIR + '/dataset_traffic_type.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['type', 'count'])
    for t, count in dataset_type.items():
        writer.writerow([t, count])


dataset_counts = dataset_count(PAPERS_DIR)

with open(OUTPUT_DIR + '/dataset_counts.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['name', 'count'])
    for n, count in dataset_counts.items():
        writer.writerow([n, count])
