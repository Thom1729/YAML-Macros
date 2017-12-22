# Standard Library

Several libraries containing useful macros are included with YAML Macros.

## arguments

The `arguments` library contains macros to access arguments passed to the engine, as well as control structures and utility functions that make use of arguments.

### `!argument(name, default=None)`

Retrieves the named argument and returns its value. If there is no argument by that name, returns `default`.

Examples:

```yaml
- !argument foo
- !argument [ foo, 42 ]
- !argument { name: foo, default: 42 }
```

### `!format(string, bindings=*)`

Performs Python's `string.format` replacement with `string` as the template and `bindings` as the arguments. If `bindings` is omitted, the current arguments are used.

### `!if(condition, then, else=None)`

Evaluates `condition`, then returns `then` if `condition` is truthy or `else` if `condition` is falsy.

### `!foreach(collection, value, *, as=None)`

For each item in `collection`, evaluate `value` with that item in the arguments. Returns an array of the results.

The name of the bound arguments is determined by `as`:

- If `as` is omitted, the item's value is bound to the argument `item`.
- If `as` is a single value, the item's value is bound to that name.

## `include`

The `include` library lets you include another YAML file.

### `!include(path)`

Includes the file located at `path`. The file should exist and should be a valid YAML file. If it uses macros, they will be evaluated. That file will inherit all of the arguments of the importing file, except that `file_path` will be set to the value of `path`. The `!include` macro will return the entirety of the included file.

### `!include_resource(path)`

As `!include`, except that `path` is interpreted as a partial path to a Sublime Text resource. The algorithm should be identical to `sublime.find_resources`; the first result will be found.

## `extend`

The `extend` library lets you modify a YAML document by applying "extensions" to it.

### `!apply(base, *extensions)`

Given a `base` value, applies each of the `extensions` to it in order.

### `!merge(items: dict)`

Returns an extension that will merge the given items into a mapping.

Example:

```yaml
!apply
- { foo: a, bar: b }
- !merge { foo: x, xyzzy: y }
```

Result:

```yaml
{ foo: x, bar: b, xyzzy: y }
```

### `!prepend(items: sequence)`

Returns an extension that will prepend the given items into a sequence.

Example:

```yaml
!apply
- [a, b, c]
- !prepend Q
- !prepend [x, y, z]
```

Result:

```yaml
[x, y, z, Q, a, b, c]
```

## `syntax`

This library facilitates writing [Sublime Text syntax definitions](http://www.sublimetext.com/docs/3/syntax.html).

### `!meta(scope: string)`

### `rule(**args)`

A utility Python function that produces a single rule with the keys in the conventional order. Used internally, but may be useful for creating your own macros.

Example:

```python
rule(
    match=r'\bfoo\b',
    scope='keyword.operator.foo',
)
```

Result:

```yaml
match: \bfoo\b
scope: keyword.operator.foo
```