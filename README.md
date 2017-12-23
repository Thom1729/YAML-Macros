NOTE: YAML Macros 3.0.0 has been released. All pre-existing functionality should be stable; however, some new features may be in flux. See the release notes for more details.

# YAML Macros

A macro system for YAML files powered by Python. Designed for Sublime Text syntax development.

## Installation

YAML Macros can be installed via [Package Control](https://packagecontrol.io/installation). You can also `git clone` this repository into your packages directory. If you do, rename it to "YAMLMacros".

## Overview

Sublime Text syntax definitions can often have a lot of boilerplate and repeated code. Consider this simple syntax that highlights SQL keywords:

```yaml
%YAML 1.2
---
name: SQL Simple (YAML Macros example)
scope: source.sql
contexts:
  main:
  - match: \b(?i:select|from|where)\b
    scope: keyword.control.sql

  - match: \b(?i:distinct|as)\b
    scope: keyword.operator.word.sql

  - match: \b(?i:dual)\b
    scope: constant.language.sql
```

The same construct `\b(?i:…)\b` is repeated over and over. This can be tedious to write and annoying to read, and in a full, complex SQL syntax with a dozen or more similar matches, it's not unlikely that a hard-to-spot typo will lead to a hard-to-detect bug, such as a keyword only working in lowercase. With YAML Macros, you can <abbr title="Don't Repeat Yourself">DRY</abbr> up your syntax by factoring out common idioms:

```yaml
%YAML 1.2
%TAG ! tag:yaml-macros:sql_simple_macros:
---
name: SQL Simple (YAML Macros example)
scope: source.sql
contexts:
  main:
    - match: !word select|from|where
      scope: keyword.control.sql

    - match: !word distinct|as
      scope: keyword.operator.word.sql

    - match: !word dual
      scope: constant.language.sql
```

Then, in `sql_simple_macros.py`:

```python
def word(str):
    return r'\b(?i:%s)\b' % str
```

It's as simple as that! For a more complex use case that uses a number of macros, see the full [SQL example](examples/sql_syntax).

## Usage

### Importing macros

To import macros into your YAML file, add a `%TAG` directive at the top referencing the file containing your macros. The syntax is as follows:

```yaml
%TAG <tag handle> tag:yaml-macros:<macro package>:
```

`<tag handle>` is the prefix you will use to invoke your macros. It must begin with an exclamation point. `<macro package>` is path to your macro definitions file. You can use multiple macro definitions files; simply write two `%TAG` directives with different tag handles.

### Invoking macros

You may invoke a macro anywhere in your YAML file a value is expected:

```
<tag handle><macro name> <value>
```

Examples:

```yaml
!word select
!expect [ ';', 'punctuation.terminator.statement.sql' ]
```

Note that there is no space between the tag handle and the name of a macro. 

### Defining macros

A macro definitions file is any Python module. It may be as simple as a single function definition or as complex as you like. If Python can do it, you can put it in a macro.

If a macro is applied to a YAML list, each list item will be passed as an argument. If a macro is applied to a YAML dictionary, each item will be passed as a keyword argument. Otherwise, the macro will receive a single value.

### Applying your macros

If you have named your file with a `.yaml-macros` extension, simply select the “YAML Macros” build system. Running the build will create a compiled YAML file at the same location without the extra `.yaml-macros` suffix.

### Command line interface

There is a basic command line interface. The CLI expects your YAML Macros file as standard input and will send the compiled YAML file to standard output. Paths will be resolved relative to your working directory.
