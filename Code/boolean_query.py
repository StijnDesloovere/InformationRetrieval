# 2.a: Implement full boolean querying supporting AND, OR and NOT.

#==============================================================================
# Posting List Intersection
#==============================================================================
def intersection(p1,p2):
    if p1 is not None and p2 is not None:
        intersection = list(set(p1) & set(p2))
        return intersection
    else:
        return []

#==============================================================================
# Posting List Union
#==============================================================================
def union(p1,p2):
    if p1 is not None and p2 is not None:
        union = list(set().union(p1,p2))
        return union
    else:
        return []

#==============================================================================
# Posting List Negation
#==============================================================================
def neg(p1,p2):
    if p1 is not None and p2 is not None:
        neg = list(set(p1) - set(p2))
        return neg
    else:
        return []


#==============================================================================
# Boolean retrieval
#==============================================================================
def boolean_retrieval():