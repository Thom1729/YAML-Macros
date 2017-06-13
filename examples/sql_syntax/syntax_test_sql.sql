-- SYNTAX TEST "Packages/YAML Macros/examples/sql_syntax/sql.sublime-syntax"

select
-- <- meta.query.sql meta.select.sql keyword.other.select.sql

distinct
-- <- keyword.other.sql

    *,
--  ^ meta.select-item.sql keyword.other.star.sql
--   ^ punctuation.separator.comma.sql - meta.select-item.sql

    2 * 2 as bar
--  ^^^^^^^^^^^^ meta.query.sql meta.select.sql meta.select-item.sql
--  ^ constant.numeric.sql
--    ^ keyword.operator.numeric.sql
--        ^^ keyword.other.sql
--           ^^^ entity.name.alias.sql

from
-- <- meta.query.sql meta.from.sql keyword.other.from.sql
    dual
--  ^^^^ meta.query.sql meta.from.sql variable.other.table.sql
;
-- <- punctuation.terminator.statement.sql - meta.query.sql




select
    "distinct" as "bar",
--  ^^^^^^^^^^ meta.string.sql
--  ^ punctuation.definition.string.begin.sql
--   ^^^^^^^^ variable.other.table.sql
--           ^ punctuation.definition.string.end.sql
--             ^^ keyword.other.sql
--                ^^^^^ meta.string.sql
--                 ^^^ entity.name.alias.sql

    "as",
--   ^^ variable.other.table.sql
--      ^ - meta.select-item.sql

    "select" "baz",
--   ^^^^^^ variable.other.table.sql
--            ^^^ entity.name.alias.sql

    xyzzy as from dual;
--           ^^^^^^^^^ meta.query.sql meta.from.sql
--           ^^^^ keyword.other.from.sql
--                ^^^^ variable.other.table.sql
--                    ^ punctuation.terminator.statement.sql - meta.query.sql