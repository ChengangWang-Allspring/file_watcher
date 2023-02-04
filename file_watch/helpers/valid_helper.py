

def has_dups_exclude_none(my_list: list) -> bool:
    # convert list to set to check if there are dups in the list
    my_list = [item for item in my_list if item is not None]
    my_set = set(my_list)
    if len(my_set) != len(my_list):
        return True
    else:
        return False
