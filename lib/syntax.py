def meta(scope):
    return [
        { "meta_scope": scope },
        { "match": r'', "pop": True },
    ]

def expect(expr, scope):
    return [
        { "match": expr, "scope": scope, "pop": True },
        { "match": r'(?=\S)', "pop": True },
    ]

def pop_on(expr):
    return {
        "match": r'(?=(?:%s))' % expr,
        "pop": True
    }

def stack(*contexts):
    return [
        {
            "match": r'(?=\S)',
            "set": contexts
        }
    ]