from YAMLMacros.lib.syntax import expect, meta, pop_on, rule, stack

__all__ = [
    # re-export macros from lib.syntax
    'expect',
    'meta',
    'pop_on',
    'rule',
    'stack',
    # define new macros
    'word',
    'identifier',
    'expect_identifier',
]


def word(string):
    return r'(?:\b(?i:%s)\b)' % string


def identifier(scope):
    return [
        rule(match=r'{{var_name}}', scope=scope, pop=True),
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
    return identifier(scope) + [rule(match=r'(?=\S)', pop=True)]
