# Usage

## Importing a Macro Library

To import a macro library into a source file, add a `%TAG` directive to the beginning of the source file, on a new line immediately following any `%YAML` directive:

```yaml
%YAML 1.2
%TAG <handle> tag:yaml-macros:<paths>:
---
…
```

*Handle* is a YAML tag handle, the prefix to use when invoking a macro later in the file. Most of the time, you should just use a single exclamation point for simplicity's sake, but you can use any valid tag handle.

*Paths* is a comma-separated list of paths to macro libraries. Python's usual path resolution mechanism is used; where it searches depends on your Python [module search path](https://docs.python.org/3/tutorial/modules.html#the-module-search-path). In case of a name conflict, macros defined in later modules will take precedence.

## Invoking a Macro

To invoke a macro in your source file, use a YAML tag corresponding to a macro you've imported:

```yaml
<handle><macro> <arguments>
```

*Handle* is a YAML tag handle defined in a `%TAG` directive. *Macro* is the name of a macro defined in a file imported in that `%TAG` directive. *Arguments* is any valid YAML value — whether a scalar, a sequence, or a mapping.

Some macros may expect a single argument; others may expect many arguments. How *arguments* is passed to the macro depends on what kind of value it is:

- If *arguments* is a scalar, it will be passed as the sole argument to the macro.
- If *arguments* is a sequence, each item in the sequence will be passed as an argument to the macro.
- If *arguments* is a mapping, each item in the sequence will be passed as a keyword argument to the macro.

## Defining a Macro Library

A macro library is a Python module. When you use a `%TAG` directive to include a library, YAML Macros will find all of the names exported from that module, with three exceptions:

- Only callable exports will be available.
- Exports beginning with an underscore will be ignored.
- Trailing underscores will be stripped. For example, an exported function named `if_` can be invoked as a macro named `if`.

When defining a macro, you should bear in mind that the user may invoke that macro with a single argument (from a scalar), with a list of arguments (from a sequence), or with keyword arguments (from a mapping).
