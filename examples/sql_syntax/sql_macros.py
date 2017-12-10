from YAMLMacros.lib.syntax import meta, expect, pop_on, stack, rule

def word(str):
    return r'(?:\b(?i:%s)\b)' % str

def identifier(scope):
    return [
        rule( match=r'{{var_name}}', scope=scope, pop=True ),
        rule(
            match=r'"',
            scope="punctuation.definition.string.begin.sql",
            set=[
                rule(meta_scope="meta.string.sql"),
                rule(meta_content_scope=scope),
                rule(match=r'"', scope="punctuation.definition.string.end.sql", pop=True),
            ],
        ),
    ] 

def expect_identifier(scope):
    return identifier(scope) + [ rule(match=r'(?=\S)', pop=True) ]