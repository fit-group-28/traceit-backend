import copy


def copyToJson(obj):
    objCopy = copy.deepcopy(obj)
    return objCopy.to_dict()
