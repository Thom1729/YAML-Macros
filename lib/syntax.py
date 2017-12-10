from collections import OrderedDict

_RULE_KEYS = ['match', 'scope', 'captures', 'push', 'set', 'pop', 'embed', 'escape', 'with_prototype']

def _rule_key_order(key):
    try:
        return _RULE_KEYS.index(key)
    except ValueError:
        return 0

def rule(**args):
    return OrderedDict(sorted(
        args.items(),
        key=lambda kv: _rule_key_order(kv[0]),
    ))

def meta(scope):
    return [
        rule(meta_scope=scope),
        rule(match=r'', pop=True),
    ]

def expect(expr, scope, set_context=None):
    ret = [
        rule(match=expr, scope=scope),
        rule(match=r'(?=\S)', pop=True),
    ]

    if set_context:
        ret[0]['set'] = set_context
    else:
        ret[0]['pop'] = True

    return ret

def pop_on(expr):
    return rule(
        match=r'(?=(?:%s))' % expr,
        pop=True
    )

def stack(*contexts):
    return [
        rule(match=r'(?=\S)', set=contexts),
    ]
