from YAMLMacros.lib.syntax import meta, expect, pop_on, stack

def word(str):
    return r'(?:\b(?i:%s)\b)' % str

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