from structures.features import Operation, Feature

op = Operation('<operation> -> {"add": [<value>+]} | {"add": [<values>]}')
# op = Operation('<operation> -> {"add": [<value>+]}')

test = Feature({'mean': ['ipTotalLength']})
# res = any([op_t(test.arguments) for op_t in op.argument_possibilities])
# print(res)

from structures.features import FeatureType

a = FeatureType('feature')
pass
