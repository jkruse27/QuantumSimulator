def isconsecutive(lst):
    """ 
    Returns True if all numbers in lst can be ordered consecutively, and False otherwise
    """
    if len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1:
        return True
    else:
        return False

