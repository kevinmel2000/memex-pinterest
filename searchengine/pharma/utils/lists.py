def split_list(list_, condition):
    """Split list into two lists based on condition"""
    true, false = [], []
    for item in list_:
        if condition(item):
            true.append(item)
        else:
            false.append(item)
    return true, false
