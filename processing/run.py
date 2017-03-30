import matplotlib.pyplot as plt
import math
import csv
from analyze import *
from analyze import _iterate_directory
from conf import PROJECT_PATH

PAPERS_DIR = PROJECT_PATH + '/data/papers'
OUTPUT_DIR = PROJECT_PATH + '/csvs'


def sort_dict(d):
    return [(k, d[k]) for k in sorted(d.keys(), key=d.__getitem__)]

def list_of_dict_to_csv(d, output_file):
    with open(output_file, 'w') as fd:
        fieldnames = d[0].keys()
        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(d)

goals = list_goals(PAPERS_DIR)
print(goals)

features = list_features(PAPERS_DIR)
print(features)

operations = list_operations(PAPERS_DIR)
print(operations)

g2f = goals_to_features(PAPERS_DIR)
print(g2f)

cit = features_to_citations(PAPERS_DIR)
srt = sort_dict(cit)
print(cit)

ops = operations_to_citations(PAPERS_DIR)
sop = sort_dict(ops)
print(ops)

ops_feat = operations_to_features(PAPERS_DIR)
print(ops_feat)

dcit = features_to_discounted_citations(PAPERS_DIR)
dsrt = sort_dict(dcit)
print(dcit)

cit_pap = features_to_nr_of_papers(PAPERS_DIR)
srt_pap = sort_dict(cit_pap)
print(cit_pap)

cit_avg = features_to_avg_citations(PAPERS_DIR)
srt_avg = sort_dict(cit_avg)
print(cit_avg)

dcit_avg = features_to_avg_discounted_citations(PAPERS_DIR)
dsrt_avg = sort_dict(dcit_avg)
print(dcit_avg)


avgs = [(k, cit_avg[k], cit[k], cit_pap[k]) for k, _ in srt_avg]
davgs = [(k, dcit_avg[k], dcit[k], cit_pap[k]) for k, _ in dsrt_avg]

all_refs = list_references(PAPERS_DIR)

citations_numbers = [r.citations for r in all_refs]
n, bins, patches = plt.hist(citations_numbers)

cit_aut = features_to_authors(PAPERS_DIR)
print(cit_aut)

cit_ref = features_to_references(PAPERS_DIR)

all = features_to_all(PAPERS_DIR)
list_of_dict_to_csv(all, OUTPUT_DIR + '/features_properties.csv')

flows_all = flow_features_to_all(PAPERS_DIR)
list_of_dict_to_csv(flows_all, OUTPUT_DIR + '/flow_features_properties.csv')

flow_keys = flow_key_features_to_all(PAPERS_DIR)
list_of_dict_to_csv(flow_keys, OUTPUT_DIR + '/flow_keys_properties.csv')

cit_goal = goals_to_feature_usage(PAPERS_DIR)
print(cit_goal)

print(len(list(list_flow_references(PAPERS_DIR))), len(list(list_references(PAPERS_DIR))))
n_flows, n_flows_w_key, n_flow_aggregations, n_packets, n = (0, 0, 0, 0, 0)
for d in _iterate_directory(PAPERS_DIR):
    has_flow = False
    has_flowkey = False
    has_flow_aggregation = False
    has_packets = False
    if 'flows' in d and d['flows'] is not None:
        for f in d['flows']:
            has_flow = True
            if 'key' in f and f['key'] is not None and 'key_features' in f['key'] and f['key']['key_features'] is not\
                    None:
                has_flowkey = True
    if 'flow_aggregations' in d and d['flow_aggregations'] is not None:
        for f in d['flow_aggregations']:
            has_flow_aggregation = True
    if 'packets' in d and d['packets'] is not None:
        for f in d['packets']:
            has_packets = True
    n += 1
    if has_flow:
        n_flows += 1
        if has_flowkey:
            n_flows_w_key += 1
    elif has_flow_aggregation:
        n_flow_aggregations += 1
    if has_packets:
        n_packets += 1
print(n_flows, n_flows_w_key, n_flow_aggregations, n_packets, n)
