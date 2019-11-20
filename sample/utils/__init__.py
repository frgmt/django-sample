def remove_duplicates_from_list(original_list):
    """ this function removes duplicates and also preserves order of the list unlike using set().
    :param original_list: list
    :return: list
    """
    # http://stackoverflow.com/a/480227
    seen = set()
    seen_add = seen.add
    return [x for x in original_list if not (x in seen or seen_add(x))]