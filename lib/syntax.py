def meta(scope):
    return [
        { "meta_scope": scope },
        { "match": r'', "pop": True },
    ]

def expect(expr, scope, set_context=None):
    ret = [
        { "match": expr, "scope": scope },
        { "match": r'(?=\S)', "pop": True },
    ]

    if set_context:
        ret[0]['set'] = set_context
    else:
        ret[0]['pop'] = True

    return ret

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