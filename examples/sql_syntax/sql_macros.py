def word(str):
    return r'(?:\b(?i:%s)\b)' % str

def meta(scope):
    return [
        { "meta_scope": scope },
        { "match": r'', "pop": True },
    ]

# def meta_set(scope):
#     return [
#         { "clear_scopes": 1 },
#         { "meta_scope": scope },
#         { "match": r'', "pop": True },
#     ]

def expect(expr, scope):
    return [
        { "match": expr, "scope": scope, "pop": True },
        { "match": r'(?=\S)', "pop": True },
    ]

def identifier(scope):
    return [
        { "match": r'{{var_name}}', "scope": scope, "pop": True },
        {
            "match": r'"',
            "scope": "punctuation.definition.string.begin.sql",
            "set": [
                {
                    "meta_scope": "meta.string.sql",
                },
                {
                    "meta_content_scope": scope,
                },
                {
                    "match": r'"',
                    "scope": "punctuation.definition.string.end.sql",
                    "pop": True,
                },
            ],
        },
    ] 

def expect_identifier(scope):
    return identifier(scope) + [ { "match": r'(?=\S)', "pop": True } ]

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